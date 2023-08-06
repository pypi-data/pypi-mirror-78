import pandas as pd
import ta
from ta.utils import dropna
from datetime import datetime, timedelta
import time
import pickle
import heapq

try:
    from .util import AlgoLogger
except:
    from util import AlgoLogger
#
#
#       Classes in algos
#
#           Algo
#           AlgoBb
#           AlgoRsi
#           AlgoRsiBb
#




class Algo:

    def __init__(self, order_manager, data_path, data_source, GUID, config):
        self.log = AlgoLogger(data_path=data_path)
        self.log.set_name(GUID)
        self.data_source = data_source
        self.GUID = GUID
        self.tickers = config["tickers"].split(",")
        self.tick_period = int(config["tick_period"])
        self.orders = []
        self.positions = {}
        order_manager.log = self.log
        self.order_manager = order_manager


    def run(self):
        self.log.info("STARTED ALGO:  " + self.GUID)
        if not bool(self.data_source.get_clock()["is_open"]):
            self.log.warn("Market is closed")
        else:
            self.log.info("Market is open")
        self.order_manager.load_algo()
        self.log.output()

    def run_end(self):
        self.log.info("Market is closed. Saving wallet data...")
        self.order_manager.save_algo()
        self.log.output()

    def print_details(self):
        return ""


class AlgoRsiBb(Algo):
    def __init__ (self, order_manager, data_path, data_source, GUID, config):
        super().__init__(order_manager, data_path, data_source, GUID,  config)
        self.data_points = int(config["data_points"])
        self.stddev = float(config["std_dev"])
        self.rsi_high = float(config["rsi_high"])
        self.rsi_low = float(config["rsi_low"])
        self.bollinger_indicator = {}
        for t in self.tickers:
            self.bollinger_indicator[t] = "Middle"

    def run(self, return_dict):
        super().run()
        trades = {}
        while bool(self.data_source.get_clock()["is_open"]):
            for t in self.tickers:
                try:
                    trades[t] += [self.data_source.get_last_trade(t)["price"]]
                except Exception as e:
                    trades[t] = [self.data_source.get_last_trade(t)["price"]]
                try:
                    if len(trades[t]) > self.data_points:
                        trades_df = pd.DataFrame(trades[t],columns=['intraday'])
                        rsi = self.generateRsiIndicator(trades_df['intraday'])
                        bollingerBands = self.generateBollingerBands(trades_df['intraday'])
                        try:
                            self.trade(t, bollingerBands, rsi)
                        except Exception as e:
                            self.log.error("Trade error: {}, {}".format(t, e))
                    else:
                        self.log.info("Init trades {}: {}".format(t, 100*len(trades[t])/self.data_points))
                except Exception as e:
                    self.log.error("dataframe issue?: {}".format(e))
            self.log.output()
            self.data_source.step(self.tick_period)
        super().run_end()
        return_dict[self.GUID] = (self.order_manager.wallet, self.positions)


    def generateBollingerBands(self, df):
        bollingerBands = ta.volatility.BollingerBands(df, n = self.data_points, ndev=self.stddev)
        return bollingerBands

    def generateRsiIndicator(self, df):
        rsi = ta.momentum.rsi(df, n = self.data_points)
        return rsi

    def trade(self, ticker, bollingerBands, rsi):
        if(bollingerBands.bollinger_hband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is above bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Above"
        elif(bollingerBands.bollinger_lband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is below bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Below"
        else:
            self.log.info("Current RSI_BB: {}  is inbetween bollinger bands; Checking RSIs : {} ".format(ticker, rsi.tail(1).iloc[0]))
            if ((rsi.tail(1).iloc[0] > 50) and (self.bollinger_indicator[ticker] == "Below")) or (rsi.tail(1).iloc[0] > self.rsi_high):
                self.order_manager.buy_shares(ticker)
            elif ((rsi.tail(1).iloc[0] < 50) and (self.bollinger_indicator[ticker] == "Above")) or (rsi.tail(1).iloc[0] > self.rsi_low):
                self.order_manager.sell_proportional(ticker)
            self.bollinger_indicator[ticker] = "Middle"
            
    def print_details(self):
        return "{}, {}, {}, {}".format(self.data_points, self.stddev, self.rsi_high, self.rsi_low)