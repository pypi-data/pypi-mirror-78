from datetime import datetime, timezone, timedelta
import time
import alpaca_trade_api as tradeapi
#
#
#       Classes in util
#
#           AlgoLogger
#           Backtester
#           Datasource
#
#

class AlgoLogger:
    def __init__(self,data_path="", name=""):
        self.to_print = []
        self.error_print = " [  -------- ERROR --------  ] "
        self.trade_print = " [  -------- TRADE --------  ] "
        self.info_print =  " [  -------- INFO  --------  ] "
        self.warn_print =  " [  -------- WARN  --------  ] "
        self.sep =         " [  -----------------------  ] "
        self.fn = data_path + "daily_logs/prog/{}.txt".format(datetime.today().strftime('%Y-%m-%d'))

    def info(self, output):
        self.to_print.append(self.info_print + str(output))
        self.output()
    def trade(self, output):
        self.to_print.append(self.trade_print + str(output))
        self.output()
    def warn(self, output):
        self.to_print.append(self.warn_print + str(output))
        self.output()
    def error(self, output):
        self.to_print.append(self.error_print + str(output))
        self.output()

    def set_name(self, name):
        self.error_print = " [ " + name + " -------- ERROR --------  ] "
        self.trade_print = " [ " + name + " -------- TRADE --------  ] "
        self.info_print =  " [ " + name + " -------- INFO  --------  ] "
        self.warn_print =  " [ " + name + " -------- WARN  --------  ] "

    def output(self):
        for p in self.to_print:
            print(p)
            try:
                log_file = open(self.fn, 'a')
                log_file.write(p)
                log_file.close()
            except:
                pass
        self.clear_print_buf()
    def output_scr(self):
        i=0
        while i < 4:
            print()
            i+=1
        self.output()
        print(self.sep * 4)
    def clear_print_buf(self):
        self.to_print = []

log = AlgoLogger()

backtest = "backtest"
live = "live"
paper = "paper"
class Backtester():
    #  date will be 'YYYY-MM-DD'
    def __init__(self, api_endpoint, tickers, start_date, end_date):
        self.api_endpoint = api_endpoint
        self.poly = api_endpoint.polygon
        tz = timezone(-timedelta(hours=4))
        self.account = 500000.0
        self.tickers = tickers
        self.is_open = True
        self.start_utc = datetime.fromisoformat(start_date).replace(tzinfo=tz).timestamp()
        self.prev_utc = None
        self.cur_time = self.start_utc
        self.end_utc = datetime.fromisoformat(end_date).replace(tzinfo=tz).timestamp()
        self.positions = {}
        self.algo_done = False
        self.cur_utc = datetime.fromtimestamp(self.cur_time, tz)
        # self.cur_utc = datetime.fromtimestamp(self.cur_time, -timedelta(hours=4))
        self.current_date = "{0:0=4d}".format(self.cur_utc.year)+"-"+"{0:0=2d}".format(self.cur_utc.month)+"-"+"{0:0=2d}".format(self.cur_utc.day)
        self.cur_df = {}
        for t in self.tickers:
            self.positions[t] = 0
        self.update_dataframes()
        self.run()

    # dictates if algo is done overall
    def run(self, tick_period):
        if self.cur_time >= self.end_utc or self.algo_done:
            self.algo_done = True
            self.is_open = False
            return
        else:
            self.run_step()

    # dictates time between market close and opens
    def run_step(self):
        minute = 60
        self.cur_time += minute
        # if it the market is closed, keep incrementing till open
        while not self.open_hours():
            self.cur_time += minute
            if self.cur_time >= self.end_utc or self.algo_done:
                self.algo_done = True
                self.is_open = False
                return

        # now check that the current data frame is valid for each ticker
        # if the dataframe isn't valid, try to get a new dataframe
        for t in self.tickers:
            valid_df = False
            while not valid_df:
                try:
                    self.cur_df[t].loc[self.cur_utc]
                    valid_df = True
                except:
                    self.cur_time += (minute * 60 * 23)
                    self.open_hours()
                    self.update_dataframes()

                    if self.cur_time >= self.end_utc or self.algo_done:
                        self.algo_done = True
                        self.is_open = False
                        return
        return
    def update_dataframes(self):
        for t in self.tickers:
            self.cur_df[t] = self.poly.historic_agg_v2(t, 1, 'minute', _from=self.current_date, to=self.current_date).df

    def open_hours(self):
        self.cur_utc = datetime.fromtimestamp(self.cur_time, timezone(-timedelta(hours=4)))
        self.current_date = "{0:0=4d}".format(self.cur_utc.year)+"-"+"{0:0=2d}".format(self.cur_utc.month)+"-"+"{0:0=2d}".format(self.cur_utc.day)
        if   (self.cur_utc.hour >= 16 and self.cur_utc.minute >= 0):
            return False
        elif (self.cur_utc.hour >= 9 and self.cur_utc.minute >= 30):
            return True
        else:
            return False

    def get_clock(self):
        return {"is_open" : self.is_open}

    def get_last_trade(self, ticker):
        price = self.cur_df[ticker].loc[self.cur_utc]
        ret = {"price" : price["close"]}
        return ret

    def get_position(self, ticker):
        ret = {"qty" : self.positions[ticker]}
        return ret

    def get_account(self):
        ret = {"cash" : self.account}
        return ret

    def submit_order(self, ticker, quantity, side, type, limit_price, time_in_force):
        # check using cur_price vs limit_price
        # cur_price = get_last_trade(ticker)
        if side == "buy":
            self.positions[ticker] += quantity
            self.account -= limit_price * quantity

        if side == "sell":
            self.positions[ticker] -= quantity
            self.account += limit_price * quantity
        return

class DataSource:

    def __init__(self, key_id, secret_key, base_url, data_source=backtest, tickers=None, start_date=None, end_date=None):

        self.api_endpoint = tradeapi.REST(
            key_id=key_id,
            secret_key=secret_key,
            base_url=base_url
        )

        self.mode = data_source      # backtest, live, paper
        self.quick_test = True
        if self.mode == backtest:
            self.backtester = Backtester(self.api_endpoint, tickers, start_date, end_date)
        else:
            self.backtester = None


    #
    # tick_perod is in seconds
    #
    def step(self, tick_period):
        if (self.mode == live or self.mode == paper):
                    if self.quick_test:
                        time.sleep(0.5)
                    else:
                        time.sleep(tick_period)
        if (self.mode == backtest):
            self.backtester.run(tick_period)


    def get_clock(self):
        if (self.mode == backtest):
            return self.backtester.get_clock()
        # if (self.mode == paper):
        #     clk = api_paper.get_clock()
        # if (self.mode == live):
        #     clk = api_live.get_clock()
        clk = self.api_endpoint.get_clock()
        ret = {"is_open" : clk.is_open}
        return ret

    def get_last_trade(self, ticker):
        if (self.mode == backtest):
            return self.backtester.get_last_trade(ticker)
        # if (self.mode == paper):
        #     trd = api_paper.get_last_trade(ticker)
        # if (self.mode == live):
        #     trd = api_live.get_last_trade(ticker)

        trd = self.api_endpoint.get_last_trade(ticker)
        ret = {"price" : trd.price}
        return ret

    def get_position(self, ticker):
        if (self.mode == backtest):
            return self.backtester.get_position(ticker)
        # if (self.mode == paper):
        #     pos = api_paper.get_position(ticker)
        # if (self.mode == live):
        #     pos = api_live.get_position(ticker)
        try:
            qty =  self.api_endpoint.get_position(ticker).qty
        except:
            qty = 0
        ret = {"qty" : qty}
        return ret

    def get_account(self):
        if (self.mode == backtest):
            return self.backtester.get_account()
        # if (self.mode == paper):
        #     act = api_paper.get_account()
        # if (self.mode == live):
        #     act = api_live.get_account()
        act = self.api_endpoint.get_account()
        ret = {"cash" : act.cash}
        return ret

    def list_orders(self, side):
        try:
            if (self.mode == backtest):
                return self.backtester.list_orders()
            if (self.mode == paper):
                orders = api_paper.list_orders()
            if (self.mode == live):
                orders = api_live.list_orders()
            valid_orders = []
            for o in orders:
                if o.side == side:
                    info = {"limit_price" : o.limit_price,
                            "qty" : o.qty,
                            "id" : o.id}
                    valid_orders.append(info)
            return valid_orders
        except Exception as e:
            print(e)
            print("list_orders : IMPLEMENT THIS")
            pass

    def submit_order(self, ticker, quantity, side, type, limit_price, time_in_force):
        try:
            if (self.mode == backtest):
                return self.backtester.submit_order(ticker, quantity, side, type, limit_price, time_in_force)
            response = self.api_endpoint.submit_order(
            symbol=ticker,
            qty=quantity,
            side=side,
            type=type,
            limit_price=limit_price,
            time_in_force=time_in_force
            )
            info = {"limit_price" : response.limit_price,
                    "qty" : response.qty,
                    "id" : response.id}
            return info

        except Exception as e:
            log.info("DATA SOURCE ERROR: submit_order()         " + str(e))
    def cancel_order(self, order_id):
        try:
            if (self.mode == backtest):
                return
            self.api_endpoint.cancel_order(
            order_id=order_id
            )
        except Exception as e:
            log.info("CANCEL ORDER ERROR: cancel_order()        " + str(e))
