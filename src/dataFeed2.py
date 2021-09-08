

import backtrader as bt
class PandasData1(bt.feeds.PandasData):
    
    lines = ("spread","eventos1","eventos2")
    params = (('spread', 5),('eventos1',6),("eventos2",7))
   
       
        
    




