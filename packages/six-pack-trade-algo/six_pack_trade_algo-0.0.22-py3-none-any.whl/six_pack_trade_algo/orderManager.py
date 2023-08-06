from datetime import datetime, timezone, timedelta
import time
import alpaca_trade_api as tradeapi
import pickle
import pandas as pd

try:
    from .util import AlgoLogger
except:
    from util import AlgoLogger


class OrderManager:
    class Memory:
        def __init__(self, tickers, wallet, positions, orders):
            self.tickers = tickers
            self.wallet = wallet
            self.positions = positions
            self.orders = orders

    def __init__(self, GUID, data_path, data_source, config, open_orders):
        self.open_orders = open_orders
        self.log = None
        self.GUID = GUID
        self.wallet = float(config["start_wallet"])
        self.threshold = float(config["thresh_percent"]) * self.wallet  
        self.data_source = data_source
        self.tickers = config["tickers"].split(",")
        self.orders = []
        self.positions = {}
        self.quick_test = True
        self.sell_percent = float(config["sell_percent"])
        self.buy_percent = float(config["buy_percent"])
        self.buy_qty = {}
        self.init_buy_price = {}
        self.init_buy = {}
        self.prev_rsi = {}
        for t in self.tickers:
            self.buy_qty[t] = int( (self.wallet*self.buy_percent) / float(self.data_source.get_last_trade(t)["price"]))
            if self.buy_qty[t] < 1:
                self.buy_qty[t] = 1
            self.init_buy_price[t] = 0
            self.init_buy[t] = True # Not used rn
            self.positions[t] = 0
        self.mem_file = data_path + "algo_mem/{}.pkl".format(GUID)

    def _buy(self, ticker, quantity, price):
        capital_out = 0
        # Goes through local order list and updates using live list
        for order in self.orders:
            if self.open_orders.get(order) != None:
                if self.open_orders[order][0] == "buy":
                    capital_out += self.open_orders[order][1] * self.open_orders[order][2]   #Add up capital_out
            else:
                self.orders.remove(order)
        # If capital out exceeds our threshold we will cancel orders starting from the oldest unitl we have enough open capital
        while capital_out > self.threshold:
            id = self.orders[0]
            side = self.open_orders[id][0]
            qty = self.open_orders[id][1]
            limit_price = self.open_orders[id][2]
            ticker = self.open_orders[id][3]
            #If the oldest order is a buy
            if side == "buy":
                self.data_source.cancel_order(id)
                total_price = qty * limit_price 
                self.wallet += total_price
                self.positions[ticker] -= qty
                self.orders.remove(id)
                capital_out -= total_price
            #If the oldest order is a sell
            else:
                self.data_source.cancel_order(id)
                total_price = qty * limit_price  
                self.wallet -= total_price
                self.positions[ticker] += qty
                self.orders.remove(id)



        if self.wallet > price:
            if not self.quick_test:
                response = self.data_source.submit_order(
                ticker=ticker,
                quantity=quantity,
                side='buy',
                type='limit',
                limit_price=price,
                time_in_force='gtc'
                )
                info = (response['id'])
                self.orders.append(info)

            self.positions[ticker] += quantity
            self.wallet -= price
            self.log.trade("Wallet Value: {}       -{}".format(self.wallet, price))
        else:
            self.log.warn(" ! NOT ENOUGH MONEY ! Wallet Value: {}".format(self.wallet))
    def _sell(self, ticker, quantity, price):
        capital_out = 0
        # Goes through local order list and updates using live list
        for order in self.orders:
            if self.open_orders.get(order) != None:
                if self.open_orders[order][0] == "sell":
                    capital_out += self.open_orders[order][1] * self.open_orders[order][2]   #Add up capital_out
            else:
                self.orders.remove(order)
        # If capital out exceeds our threshold we will cancel orders starting from the oldest unitl we have enough open capital
        while capital_out > self.threshold:
            id = self.orders[0]
            side = self.open_orders[id][0]
            qty = self.open_orders[id][1]
            limit_price = self.open_orders[id][2]
            ticker = self.open_orders[id][3]
            #If the oldest order is a buy
            if side == "buy":
                self.data_source.cancel_order(id)
                total_price = qty * limit_price 
                self.wallet += total_price
                self.positions[ticker] -= qty
                self.orders.remove(id)    
            #If the oldest order is a sell
            else:
                self.data_source.cancel_order(id)
                total_price = qty * limit_price  
                self.wallet -= total_price
                self.positions[ticker] += qty
                self.orders.remove(id)
                capital_out -= total_price



        if self.positions[ticker] >= quantity:
            if not self.quick_test:
                response = self.data_source.submit_order(
                ticker=ticker,
                quantity=quantity,
                side='sell',
                type='limit',
                limit_price=price,
                time_in_force='gtc'
                )
                info = (response['id'])
                self.orders.append(info)

            self.positions[ticker] -= quantity
            self.wallet += price
            self.log.trade("Wallet Value: {}       +{}".format(self.wallet, price))
        else:
            self.log.warn(" ! NOT ENOUGH SHARES ! Wallet Value: {}".format(self.wallet))
    def save_algo(self):
        try:
            if self.quick_test: raise Exception("Test mode on. No Saving.")
            fs = open(self.mem_file ,"w+b")
            to_save = self.Memory(self.tickers, self.wallet, self.positions, self.orders)
            pickle.dump(to_save,fs)
            fs.close()
            self.log.info("MEM_SAVE SUCCESSFUL")
        except Exception as e:
            self.log.error("Cannot save algo: ")
            self.log.error(e)

    def load_algo(self):
        if self.quick_test: return
        try:
            fs = open(self.mem_file ,"rb")
            from_save = pickle.load(fs)
            if self.tickers != from_save.tickers:
                raise Exception("Incompatable ticker found in mem. Resetting...")
            self.wallet = from_save.wallet
            self.positions = from_save.positions
            self.orders = from_save.orders
            self.log.info("Found Memory ||     wallet:{}".format(self.wallet))
            fs.close()
        except Exception as e:
            self.log.warn("Cannot load algo. Creating a mem file...   "   + str(e))
            self.save_algo()
    def sell_proportional(self, ticker):
        # Check sell queue for too many open orders. Update wallet accordingly
        # orders = self.data_source.list_orders('sell')
        # total_investment_out = 0
        # new_orders = []
        # for order in orders:
        #     if(self.orders.find(order['id'])):
        #         new_orders.append(self.orders[order['id']]) #add orders that are still open to new list
        #         total_investment_out += order['qty'] * order['limit_price']
        # self.orders = new_orders
        # while total_investment_out > self.threshold: #Cancel oldest current open order on this process (front)
        #
        try:
            self.log.info("sell_proportional {}".format(ticker))
            pos = self.data_source.get_position(ticker)
            price = self.data_source.get_last_trade(ticker)["price"]
            if pos["qty"] == 0:
                self.log.info("sell_proportional no shares to sell")
                return
            if int(pos["qty"]) <= 30:
                qty = int(pos["qty"])
            else:
                qty = int(float(pos["qty"])*(self.sell_percent))
                if(qty == 0):
                    self.log.info("sell_proportional no shares to sell")
                    return
            self._sell(ticker, qty, float(price))
            self.log.info("SELL Partial {} shares of {}".format(qty, ticker))
        except Exception as e:
            self.log.error("sell_proportional error: {} ".format(e))

    def buy_shares(self, ticker):
        try:
            self.log.info("buy_shares {}".format(ticker))
            # Make sure that the current wallet value - (buy price * qty + 1%)  > 25,000
            balance = float(self.data_source.get_account()["cash"])
            price = float(self.data_source.get_last_trade(ticker)["price"])
            total_cost = price * float(self.buy_qty[ticker])
            if (balance - (total_cost * 1.01)> 25000.0):
                self._buy(ticker, self.buy_qty[ticker], price)
                self.log.info("BUY {} shares of {}".format(self.buy_qty[ticker], ticker))
            else:
                raise Exception("Not enough wallet value. Cost:{} / Balance:{}".format(total_cost, balance))
        except Exception as e:
            self.log.error("buy_shares error: {}".format(e))
            
    def print_details(self):
        return "{}, {}".format(self.buy_percent, self.sell_percent)