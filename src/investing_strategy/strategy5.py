import datetime as dt
import v20
import backtrader as bt
import time
import numpy as np
CONSTANTE=-100000
CAP_INICIAL=90000
class TestStrategy(bt.Strategy):
    #dont use log=True with optimation stratey
    params = (('print',False),('maxEntries',10),('log',False),('lookBack',4),('MAperiodShort',8),('MAperiodLong',22),('MAperiodShort2',8),('MAperiodLong2',22),('symbols',[]),('events',{}),('paramStopLoss',0.25))
    
    def log(self, txt, dt=None):
      if self.params.log:
        dt = dt or self.datas[0].datetime.datetime(0)
        try:
           
            self.f.write('%s, %s' % (dt, txt) + "\n")
        except Exception as e:
            print(e)
    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash,2)
        
        print('Final PnL: {}, tamAcumlado {}, max drowdowns {}, capital minimo {}, max invested {}'.format(pnl,self.tamAcumulado,self.caida,self.minProfit,self.minMargin))
        
      
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
        self.maximaGanancia= CAP_INICIAL/30
        self.caida=0
        #print("Numero de simbolos %s"%((len(self.datas))))
        self.tamAcumulado=0
        self.dineroInicialOperacion=0
        self.minProfit=100000
        self.minMargin=0
      
        for i in range(len(self.datas)):
            
           
            self.mas1Short.append([])
            self.mas2Short.append([])
            self.mas1Long.append([])
            self.mas2Long.append([])
            self.data1.append([])
            self.data2.append([])
            self.ks.append(0)
            self.buyBefore.append(False)
            self.sellBefore.append(False)
            for k in range(len(self.params.events[self.params.symbols[i].split("_")[0]])):
                self.mas1Short[i].append(0)
                self.mas2Short[i].append(0)
                self.mas1Long[i].append(0)
                self.mas2Long[i].append(0)
                self.data1[i].append([])
                self.data2[i].append([])
        self.mas1Short = np.array(self.mas1Short,dtype=object)
        self.mas2Short = np.array(self.mas2Short,dtype=object)
        
        self.mas1Long = np.array(self.mas1Long,dtype=object)
        self.mas2Long= np.array(self.mas2Long,dtype=object)
        
            
    def calculateMeans(self,i,k,symbol):
        """if self.datas[0].datetime.datetime(0)==dt.datetime(2015,6, 18):
                print(np.array((self.data1[i][k][-self.params.MAperiodShort:])))
                print(np.array((self.data1[i][k][-self.params.MAperiodLong:])))
                
                print(np.array((self.data1[i][k][-self.params.MAperiodShort:])).mean()-np.array((self.data1[i][k][-self.params.MAperiodLong:])).mean())
                time.sleep(5)"""
                
        if symbol==1:
           
        
            self.mas1Short[i][k]=np.array((self.data1[i][k][-self.params.MAperiodShort:])).mean()
           
            self.mas1Long[i][k]=np.array((self.data1[i][k][-self.params.MAperiodLong:])).mean()
            
          
           
      
        else:
             self.mas2Short[i][k]=np.array((self.data2[i][k][-self.params.MAperiodShort2:])).mean()
             self.mas2Long[i][k]=np.array((self.data2[i][k][-self.params.MAperiodLong2:])).mean()
             
      
    def checkConditions(self,i,k):


        if len(self.data1[i][k])>=self.params.lookBack and len(self.data2[i][k])>=self.params.lookBack:
            if self.mas1Short[i][k]>self.mas1Long[i][k] and self.mas2Short[i][k]<self.mas2Long[i][k]:
                self.log("difrencia1 %s,diferencia 2 %s"%(self.mas1Short[i][k]-self.mas1Long[i][k],self.mas2Short[i][k]-self.mas2Long[i][k],))
                if self.params.print:
                 
                    print (("%s, Buy because of means: first symbol short mean %s, first symbol long mean %s, "
                   "second symbol short mean %s, second symbol long mean %s")%(self.datas[0].datetime.datetime(0),self.mas1Short[i][k],self.mas1Long[i][k],self.mas2Short[i][k],self.mas2Larga[i][k]))
                return "buy"
            elif self.mas1Short[i][k]<self.mas1Long[i][k] and self.mas2Short[i][k]>self.mas2Long[i][k]:
              self.log("difrencia1 %s,diferencia 2 %s"%(self.mas1Short[i][k]-self.mas1Long[i][k],self.mas2Short[i][k]-self.mas2Long[i][k],))
              if self.params.print:
                print (("%s, Sell because of means: first symbol short mean %s, first symbol long mean %s, "
                   "second symbol short mean %s, second symbol long mean %s")%(self.datas[0].datetime.datetime(0),self.mas1Short[i][k],self.mas1Long[i][k],self.mas2Short[i][k],self.mas2Long[i][k]))
              return "sell"
           
        
        
        return "no action"
    
    def checkInterestRate(self,comprar):
        if comprar==True:
            if self.data2[0][2][-1]<=50 and np.mean((self.data2[0][2][-4:]))>np.mean((self.data2[0][2][-1:])):
                print("%s Nada de compras "%(self.datas[0].datetime.datetime(0)))
                return False
            return True
        else:
             if self.data2[0][2][-1]>=350:
                print("Nada de ventas %s"%(self.datas[0].datetime.datetime(0)))
                return False
             return True
            
        
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
                """print("BUY EXECUTED, Price: %.5f, Cost: %.2f, Comm %.2f %s" %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                           self.datas[0].datetime.datetime(0)))"""
            
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.5f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                """print("SELL EXECUTED, Price: %.5f, Cost: %.2f, Comm %.2f %s" %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                           self.datas[0].datetime.datetime(0)))"""
            self.bar_executed = len(self)


        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            print('Order Canceled/Margin/Rejected %s, %s, %s' %(self.datas[0].datetime.datetime(0),(self.broker.get_value()-87000),(self.getposition(self.datas[0]).size)))
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.5f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        """print('OPERATION PROFIT, GROSS %.5f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))"""

    def next(self):
        totalSize=0
        #print(self.datas[0].datetime.datetime(0))
       
        #print(self.getposition(self.datas[0]).size*(self.datas[0].close[0]-self.getposition(self.datas[0]).price))
        
        if (self.broker.get_value()-87000-10000000)<self.minProfit:
            self.minProfit=(self.broker.get_value()-87000-10000000)
        if self.order:
            return
        cantidadInvertida=abs(self.getposition(self.datas[0]).size)*self.datas[0].close[0]
        cantidadInvertida=cantidadInvertida/30/(self.broker.get_value()-self.startcash+3000)
        if cantidadInvertida>self.minMargin:
            self.minMargin=cantidadInvertida
        #print("Cantidad invertida %s"%cantidadInvertida)
        #time.sleep(0.01)
        if (CAP_INICIAL/30+(self.broker.get_value()-self.startcash)>self.maximaGanancia):
           
            self.maximaGanancia=CAP_INICIAL/30+(self.broker.get_value()-self.startcash)
            #print("Max profit alcanzado el dia %s:capital %s, drowdown %s"%(str(self.datas[0].datetime.datetime(0)),(CAP_INICIAL/30+(self.broker.get_value()-self.startcash)),self.caida))
            #time.sleep(0.1)
        if self.maximaGanancia-(CAP_INICIAL/30+(self.broker.get_value()-self.startcash))>self.caida:
           
            self.caida=self.maximaGanancia-(CAP_INICIAL/30+(self.broker.get_value()-self.startcash))
            #print("Max drowdown alcanzado el dia %s:capital %s, drowdown %s"%(str(self.datas[0].datetime.datetime(0)),(CAP_INICIAL/30+(self.broker.get_value()-self.startcash)),self.caida))
            
        
        #if(3000+(self.broker.get_value()-90000)>10000):
            #time.sleep(1)
        #print(self.datas[0].datetime.datetime(0).weekday())
        #print(self.broker.get_value()-87000)
        #time.sleep(0.02)
        uu=(self.broker.get_value()-87000-10000000)
        #print(self.dineroInicialOperacion)
        if self.dineroInicialOperacion>0 and abs(self.getposition(self.datas[0]).size)>0 and ((self.dineroInicialOperacion-uu)/self.dineroInicialOperacion)>self.params.paramStopLoss:
               self.order = self.close(data=self.datas[0])    
        for i in range(len(self.datas)):
           if self.datas[0].datetime.datetime(0).weekday()==2:
               if self.getposition(self.datas[i]).size<0:
                self.tamAcumulado+=abs(3*self.getposition(self.datas[i]).size )
           else:
               self.tamAcumulado+=abs(self.getposition(self.datas[i]).size )
                 
           symbol1_2=self.params.symbols[i].split("_")
           symbol1=symbol1_2[0]
           symbol2=symbol1_2[1]
           events1=self.params.events[symbol1]
           events2=self.params.events[symbol2]
           totalSize+=abs(self.getposition(self.datas[i]).size)
           k=0
           u=0
           lll=0
           for e1,e2 in zip(events1,events2):
              
               lll+=1
               event1=e1+str(0)
               event2=e2+str(1)
               #print(event1)
               #print(event2)
              
               a=self.broker.get_value()-10000000-90000-self.getposition(self.datas[i]).size*(self.datas[i].close[0]-self.getposition(self.datas[i]).price)
               a=a*30
               
               #if a>=0:
               #size =  self.broker.get_value()  / (10*len(self.datas)*self.params.maxEntries)
               size =  (a+90000)  / (3*len(self.datas)*self.params.maxEntries)
               
               #else:
                    # size =  (90000)  / (3*len(self.datas)*self.params.maxEntries)
                   
               sizeToBuy = int(size / (self.datas[i].close[0]))
              
               #sizeToBuy=max([sizeToBuy,sizeToBuy *3-abs(self.getposition(self.datas[i]).size)])
               #print(sizeToBuy)
               #if(self.getposition(self.datas[i]).size ==0):
                           
                   #     sizeToBuy1=2* sizeToBuy
               comision = 0.5 * (getattr(self.datas[i],"spread"))[0] / (self.datas[i].close[0])
               
               self.broker.setcommission(commission=comision, name=self.params.symbols[i])
             
               
               #print(("%s %s %s"%(k,self.mas1Short[i][k],self.params.symbols[i])))
               if self.buyBefore[i] :
                      self.dineroInicialOperacion=self.broker.get_value()-10000000-90000+3000
                    
                      if self.getposition(self.datas[i]).size < 0:
                                     self.order = self.close(data=self.datas[i])
                                     self.ks[i]=0
                      if self.ks[i]<self.params.maxEntries:           
                        self.order = self.buy(self.datas[i], size=sizeToBuy)
                        #self.ks[i]+=1
                      self.buyBefore[i]=False               
               if self.sellBefore[i] :
                    self.dineroInicialOperacion=self.broker.get_value()-10000000-90000+3000
                  
                    #self.log("CLose %s"%((self.datas[i].close[0])))
                    #self.log("Comision %s"%(comision))
                    #self.log("SIze to buy %s"%(sizeToBuy))
                    if self.getposition(self.datas[i]).size > 0:
                                     self.order = self.close(data=self.datas[i])
                                     self.ks[i]=0
                    if self.ks[i]<self.params.maxEntries: 
                         self.order = self.sell(self.datas[i], size=sizeToBuy)
                         #self.ks[i]+=1
                    self.sellBefore[i]=False                    
               if getattr(self.datas[i],event1)[0]!=0 or  getattr(self.datas[i],event2)[0]!=0:
                   if getattr(self.datas[i],event1)[0]!=0:
                       if getattr(self.datas[i],event1)[0]!=CONSTANTE:
                           self.data1[i][k].append(getattr(self.datas[i],event1)[0])
                       else:
                            #print("cte")
                            self.data1[i][k].append(0)
                       self.calculateMeans(i,k,1)
                   if  getattr(self.datas[i],event2)[0]!=0:   
                        if getattr(self.datas[i],event2)[0]!=CONSTANTE:
                            self.data2[i][k].append(getattr(self.datas[i],event2)[0])
                        else:
                            #print("cte")
                            self.data2[i][k].append(0)
                        self.calculateMeans(i,k,2)
                   if lll<3:
                       action=self.checkConditions(i,k)
                       if action=="buy" and u==0 :
                           self.buyBefore[i]=True
                           self.log("buy before")
                           """if self.getposition(self.datas[i]).size < 0:
                                         self.order = self.close(data=self.datas[i])
                                         self.ks[i]=0
                           if self.ks[i]<self.params.maxEntries:           
                            self.order = self.buy(self.datas[i], size=sizeToBuy)
                            #self.ks[i]+=1
                           self.buyBefore[i]=False  """
                           u=1
                           
                        
                       elif action=="sell" and u==0 :
                           self.sellBefore[i]=True
                           self.log("sell before")
                           """if self.getposition(self.datas[i]).size > 0:
                                         self.order = self.close(data=self.datas[i])
                                         self.ks[i]=0
                           if self.ks[i]<self.params.maxEntries: 
                             self.order = self.sell(self.datas[i], size=sizeToBuy)
                             #self.ks[i]+=1
                           self.sellBefore[i]=False """
                           u=1
               k+=1     
        #print(totalSize)