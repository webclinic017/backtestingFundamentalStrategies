import datetime as dt
import v20
import backtrader as bt
import time
import numpy as np

class TestStrategy(bt.Strategy):
    #dont use log=True with optimation stratey
    params = (('print',False),('maxEntradas',10),('log',False),('lookBack',4),('MAperiodShort',5),('MAperiodLong',12),('maximoCPI',200),('symbols',[]),('events',{}))
    
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
            self.f = open("fichero.txt", "w")
       
        self.order = None
        self.mas1Corta = []
        self.mas2Corta = []
        self.datos1=[]
        self.mas1Larga = []
        self.mas2Larga = []
        self.datos2=[]
        self.ks=[]
        self.anteriorCompra=[]
        self.anteriorVenta=[]
        #print("Numero de simbolos %s"%((len(self.datas))))
        
        for i in range(len(self.datas)):
            
            
            self.mas1Corta.append(0)
            self.mas2Corta.append(0)
            self.mas1Larga.append(0)
            self.mas2Larga.append(0)
            self.datos1.append([])
            self.datos2.append([])
            self.ks.append(0)
            self.anteriorCompra.append(False)
            self.anteriorVenta.append(False)
        print(self.params.events)
        print("Init terminado")
        
            
    def calcularMedias(self,i,simbolo):
        if simbolo==1:
            
            self.mas1Corta[i]=np.array((self.datos1[i][-self.params.MAperiodShort:])).mean()
           
            self.mas1Larga[i]=np.array((self.datos1[i][-self.params.MAperiodLong:])).mean()
           
      
        else:
             self.mas2Corta[i]=np.array((self.datos2[i][-self.params.MAperiodShort:])).mean()
             self.mas2Larga[i]=np.array((self.datos2[i][-self.params.MAperiodLong:])).mean()
      
    def comprobarCondiciones(self,i):
        """print(self.mas1Corta)
        print(self.mas1Larga)
        print(self.mas2Corta)
        print(self.mas2Larga)
        print("-----")"""
       
        if len(self.datos1[i])>=self.params.lookBack and len(self.datos2[i])>=self.params.lookBack:
            if self.mas1Corta[i]>self.mas1Larga[i] and self.mas2Corta[i]<self.mas2Larga[i]:
                if self.params.print:
                   
                    print (("%s, Compra por medias: media corta del primero simbolo= %s, media larga del primer simbolo= %s, "
                    "media corta del segundo simbolo= %s, media larga del segundo simbolo= %s")%(self.datas[0].datetime.datetime(0),self.mas1Corta[i],self.mas1Larga[i],self.mas2Corta[i],self.mas2Larga[i]))
                return "compra"
            elif self.mas1Corta[i]<self.mas1Larga[i] and self.mas2Corta[i]>self.mas2Larga[i]:
              if self.params.print:
                print (("%s, Venta por medias: media corta del primero simbolo= %s, media larga del primer simbolo= %s,"
                "media corta del segundo simbolo= %s, media larga del segundo simbolo= %s")%(self.datas[0].datetime.datetime(0),self.mas1Corta[i],self.mas1Larga[i],self.mas2Corta[i],self.mas2Larga[i]))
              return "venta"
            
            """if self.datos1[i][-self.params.lookBack]==self.params.maximoCPI:
                if self.params.print:
                    print(self.datas[0].datetime.datetime(0))
                    print("compra por maximo")
                return "compra"
            elif self.datos2[i][-self.params.lookBack]==self.params.maximoCPI:
                if self.params.print:
                    print(self.datas[0].datetime.datetime(0))
                    print("venta por maximo")
                return "venta"""
        
        
        return "nada"
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
        cantidadTotal=0
     
        if self.order:
            return
        
        for i in range(len(self.datas)):
           symbol1_2=self.params.symbols[i].split("_")
           symbol1=symbol1_2[0]
           symbol2=symbol1_2[1]
           events1=self.params.events[symbol1]
           events2=self.params.events[symbol2]
           #print(events1)
           cantidadTotal+=abs(self.getposition(self.datas[i]).size)
           k=0
           for e1,e2 in zip(events1,events2):
              if k==0: 
               event1=e1+str(0)
               event2=e2+str(1)
               #print("%s %s %s"%(self.params.symbols[i],event1,event2))
              
               
               
           
               
              
               cantidad =  self.broker.get_value()  / (len(self.datas)*self.params.maxEntradas)
             
               cantidadAComprar = int(cantidad / (self.datas[i].close[0]))
                
               comision = 0.5 * (getattr(self.datas[i],"spread"))[0] / (self.datas[i].close[0])
               """if (getattr(self.datas[i],event2))[0]!=0 and symbol2=="USD":
                   print("%s %s %s %s %s"%(i,self.datas[0].datetime.datetime(0),symbol1,(getattr(self.datas[i],event2))[0],event2))
                   time.sleep(1)"""
               self.broker.setcommission(commission=comision, name=self.params.symbols[i])
               if self.anteriorCompra[i]:
                      if self.getposition(self.datas[i]).size < 0:
                                     self.order = self.close(data=self.datas[i])
                                     self.ks[i]=0
                      if self.ks[i]<self.params.maxEntradas:           
                        self.order = self.buy(self.datas[i], size=cantidadAComprar)
                        #self.ks[i]+=1
                      self.anteriorCompra[i]=False               
               if self.anteriorVenta[i]:
                    if self.getposition(self.datas[i]).size > 0:
                                     self.order = self.close(data=self.datas[i])
                                     self.ks[i]=0
                    if self.ks[i]<self.params.maxEntradas: 
                         self.order = self.sell(self.datas[i], size=cantidadAComprar)
                         #self.ks[i]+=1
                    self.anteriorVenta[i]=False                     
               if getattr(self.datas[i],event1)[0]!=0 or  getattr(self.datas[i],event2)[0]!=0:
                   if getattr(self.datas[i],event1)[0]!=0:
                       self.datos1[i].append(getattr(self.datas[i],event1)[0])
                       self.calcularMedias(i,1)
                   if  getattr(self.datas[i],event2)[0]!=0:   
                        self.datos2[i].append(getattr(self.datas[i],event2)[0])
                        self.calcularMedias(i,2)
                   accion=self.comprobarCondiciones(i)
                   if accion=="compra":
                       self.anteriorCompra[i]=True
                       break
                       
                    
                   elif accion=="venta":
                       self.anteriorVenta[i]=True
                       break
              k+=1     
        #print(cantidadTotal)