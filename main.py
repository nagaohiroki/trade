import datetime
import backtrader
import pandas_datareader


class MyStrategy(backtrader.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'buy executed {order.executed.price}')
            elif order.issell():
                self.log(f'sell executed {order.executed.price}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order Canceled/Margin/Rejected')
        self.order = None

    def next(self):
        self.log(f'Close {self.dataclose[0]}')
        if self.order:
            return
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                   self.log(f'buy create {self.dataclose[0]}')
                   self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log(f'SELL CREATE {self.dataclose[0]}')
                self.order = self.sell()


def get_data():
    data = backtrader.feeds.YahooFinanceCSVData(
        dataname='datas/yhoo-2014.txt',
        fromdata=datetime.datetime(2014, 1, 2),
        todate=datetime.datetime(2014, 12, 1),
        reverse = False)
    return data

def get_data_():
    df = pandas_datareader.DataReader('AAPL', 'stooq', '2023-01-02', '2023-12-31')
    df.to_csv('datas/AAPL.csv')

def run():
    cerebro = backtrader.Cerebro()
    cerebro.addstrategy(MyStrategy)
    data = get_data()
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue()}')
    cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue()}')


def main():
    run()


if __name__ == '__main__':
    main()
