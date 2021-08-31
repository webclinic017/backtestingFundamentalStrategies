import backtrader as bt
class PandasData1(bt.feeds.PandasData):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''
    lines = ("spread","eventos1","eventos2")
    params = (('spread', 5),('eventos1',6),("eventos2",7))
    


# symbols=["USD_ZAR","ZAR_JPY"]


