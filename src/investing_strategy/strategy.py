import datetime as dt
import v20
import backtrader as bt
import time
import numpy as np

class TestStrategy(bt.Strategy):
    #dont use log=True with optimation stratey
    params = (('print',False),('maxEntries',10),('log',True),('lookBack',4),('MAperiodShort',5),('MAperiodLong',12),('symbols',[]),('events',{}))
    
    def log(self, txt, dt=None):
      if self.params.log:
        dt = dt or self.datas[0].datetime.datetime(0)
        try:
           
            self.f.write('%s, %s' % (dt, txt) + "\n")
        except Exception as e:
            print(e)
    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash,2)
        print('Final PnL: {}'.format(pnl))
      
    def __init__(self):
        self.startcash = self.broker.getvalue()
        if self.params.log:
            self.f = open("./investing_strategy/results/orderLog.txt", "w")
       
        self.order = None
        self.mas1Short = []
        self.mas2Short = []
        self.data1=[]
        self.mas1Long = []
        self.mas2Long= []
        self.data2=[]
        self.ks=[]
        self.buyBefore=[]
        self.sellBefore=[]
        #print("Numero de simbolos %s"%((len(self.datas))))
        
        for i in range(len(self.datas)):
            
            
            self.mas1Short.append(0)
            self.mas2Short.append(0)
            self.mas1Long.append(0)
            self.mas2Long.append(0)
            self.data1.append([])
            self.data2.append([])
            self.ks.append(0)
            self.buyBefore.append(False)
            self.sellBefore.append(False)
       
        
            
    def calculateMeans(self,i,symbol):
        if symbol==1:
        
            self.mas1Short[i]=np.array((self.data1[i][-self.params.MAperiodShort:])).mean()
           
            self.mas1Long[i]=np.array((self.data1[i][-self.params.MAperiodLong:])).mean()
           
      
        else:
             self.mas2Short[i]=np.array((self.data2[i][-self.params.MAperiodShort:])).mean()
             self.mas2Long[i]=np.array((self.data2[i][-self.params.MAperiodLong:])).mean()
      
    def checkConditions(self,i):

       
        if len(self.data1[i])>=self.params.lookBack and len(self.data2[i])>=self.params.lookBack:
            if self.mas1Short[i]>self.mas1Long[i] and self.mas2Short[i]<self.mas2Long[i]:
                if self.params.print:
                   
                    print (("%s, Buy because of means: first symbol short mean %s, first symbol long mean %s, "
                   "second symbol short mean %s, second symbol long mean %s")%(self.datas[0].datetime.datetime(0),self.mas1Short[i],self.mas1Long[i],self.mas2Short[i],self.mas2Larga[i]))
                return "buy"
            elif self.mas1Short[i]<self.mas1Long[i] and self.mas2Short[i]>self.mas2Long[i]:
              if self.params.print:
                print (("%s, Sell because of means: first symbol short mean %s, first symbol long mean %s, "
                   "second symbol short mean %s, second symbol long mean %s")%(self.datas[0].datetime.datetime(0),self.mas1Short[i],self.mas1Long[i],self.mas2Short[i],self.mas2Long[i]))
              return "sell"
           
        
        
        return "no action"
    def notify_order(self, order):
        
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.5f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.5f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)


        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.5f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        totalSize=0
     
        if self.order:
            return
        
        for i in range(len(self.datas)):
           symbol1_2=self.params.symbols[i].split("_")
           symbol1=symbol1_2[0]
           symbol2=symbol1_2[1]
           events1=self.params.events[symbol1]
           events2=self.params.events[symbol2]
           totalSize+=abs(self.getposition(self.datas[i]).size)
           k=0
           for e1,e2 in zip(events1,events2):
              if k==0: 
               event1=e1+str(0)
               event2=e2+str(1)
               size =  self.broker.get_value()  / (len(self.datas)*self.params.maxEntries)
             
               sizeToBuy = int(size / (self.datas[i].close[0]))
                
               comision = 0.5 * (getattr(self.datas[i],"spread"))[0] / (self.datas[i].close[0])
               self.broker.setcommission(commission=comision, name=self.params.symbols[i])
               if self.buyBefore[i]:
                      if self.getposition(self.datas[i]).size < 0:
                                     self.order = self.close(data=self.datas[i])
                                     self.ks[i]=0
                      if self.ks[i]<self.params.maxEntries:           
                        self.order = self.buy(self.datas[i], size=sizeToBuy)
                        #self.ks[i]+=1
                      self.buyBefore[i]=False               
               if self.sellBefore[i]:
                    if self.getposition(self.datas[i]).size > 0:
                                     self.order = self.close(data=self.datas[i])
                                     self.ks[i]=0
                    if self.ks[i]<self.params.maxEntries: 
                         self.order = self.sell(self.datas[i], size=sizeToBuy)
                         #self.ks[i]+=1
                    self.sellBefore[i]=False                     
               if getattr(self.datas[i],event1)[0]!=0 or  getattr(self.datas[i],event2)[0]!=0:
                   if getattr(self.datas[i],event1)[0]!=0:
                       self.data1[i].append(getattr(self.datas[i],event1)[0])
                       self.calculateMeans(i,1)
                   if  getattr(self.datas[i],event2)[0]!=0:   
                        self.data2[i].append(getattr(self.datas[i],event2)[0])
                        self.calculateMeans(i,2)
                   action=self.checkConditions(i)
                   if action=="buy":
                       self.buyBefore[i]=True
                       break
                       
                    
                   elif action=="sell":
                       self.sellBefore[i]=True
                       break
              k+=1     
        #print(totalSize)