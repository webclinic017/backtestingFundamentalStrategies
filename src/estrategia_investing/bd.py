# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 15:38:26 2021

@author: Manuel
"""
import mysql.connector
import math
import pandas as pd
import datetime as dt
HOST="localhost"
USER="root"
PASSWORD=
PORT= 33063
DATABASE="bolsa"

class  Bd():
    
    
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=HOST,
            user=USER,
            port=PORT,
            password=PASSWORD,database=DATABASE
            )
        self.mycursor = self.mydb.cursor()
        
    def añadirAnalisis(self,periodicidad,row,desde,hasta,H,media,fuller,fullerEstimacion,array=[]):
        f = '%Y-%m-%d %H:%M:%S'
        tupla=(str(periodicidad),str(row),(desde),(hasta),float(H),float(media),float(fuller))
        cadena="(%s,%s,%s,%s,%s,%s,%s,%s,%s"
        for t in array:
            cadena+=",%s"
            tupla=tupla.__add__((float(t),))
        cadena+=")"
        tupla=tupla.__add__((float(fullerEstimacion),))
        coc=math.log(2)/(float(fullerEstimacion))
        tupla=tupla.__add__((coc,))
        self.mycursor.execute("INSERT INTO analisisEstacionaridad VALUES"+cadena,tupla)
        self.mydb.commit()
    def añadirAnalisisCorr(self,periodicidad,row,symbol1,desde,hasta,H,media,fuller,fullerEstimacion,array):
        f = '%Y-%m-%d %H:%M:%S'
        tupla=(str(periodicidad),str(row),str(symbol1),(desde),(hasta),float(H),float(media),float(fuller))
        cadena="(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
        for t in array:
            cadena+=",%s"
            tupla=tupla.__add__((float(t),))
        cadena+=")"
        tupla=tupla.__add__((float(fullerEstimacion),))
        coc=math.log(2)/(float(fullerEstimacion))
        tupla=tupla.__add__((coc,))
        self.mycursor.execute("INSERT INTO analisisEstacionaridadCorr VALUES"+cadena,tupla)
        self.mydb.commit()
    
    def getSimbolos(self,periodicidad,fecha,fuller=0.1,H=0.5,var=0.1):
        self.mycursor.execute("SELECT symbol from  analisisEstacionaridad where periodicidad=%s AND date1= %s and fuller<%s and hurst<%s and (var1<%s or var2<%s or var3<%s)",(periodicidad,fecha,fuller,H,var,var,var))
        myresult = self.mycursor.fetchall()
        symbols=[]
        for x in myresult:
           
            symbols.append(x[0])
        return symbols
    def getSimbolosPorHurst(self,periodicidad,fecha1,fecha2,fuller=0.1,H=0.5):
     
        self.mycursor.execute("SELECT symbol,half_life from  analisisEstacionaridad where periodicidad=%s AND date1= %s AND date2=%s and fuller<=%s and hurst<%s",(periodicidad,fecha1,fecha2,fuller,H))
        myresult = self.mycursor.fetchall()
        symbols=[]
        h=[]
        for x in myresult:
           
            symbols.append(x[0])
            h.append(x[1])
            
        return symbols,h
    def anadirResultadoBacktesing(self,idEstrategia,date1,date2,date1Estra,date2Estra,symbol,periodicidad,beneficio,drawdawn,sharpe,symbol2):
        self.mycursor.execute("INSERT INTO resultadosBacktesting VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (idEstrategia,date1,date2,date1Estra,date2Estra,symbol,periodicidad,float(beneficio),float(sharpe),float(drawdawn),str(symbol2),))

        self.mydb.commit()

    def añadirCalendario(self,id,date,zone,currency,importance,event,actual,forecast,previous):
        f = '%Y-%m-%d %H:%M:%S'
        tupla = (id, date, zone,currency,importance,event,actual,forecast,previous)
        cadena = "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"


        self.mycursor.execute("INSERT INTO calendario VALUES" + cadena, tupla)
        self.mydb.commit()

    def obtenerPorEventos(self,evento:str):
        evento=evento[:-1]
        self.mycursor.execute("select * from calendario where event like %s",('%'+evento+'%',))
        df = pd.DataFrame(self.mycursor.fetchall())
        df.columns = self.mycursor.column_names
        return df
    
    def obtenerPorEventosYFechas(self,evento:str,fecha1:str,fecha2:str):
        evento=evento[:-1]
        self.mycursor.execute("select * from calendario where event like %s and fecha>= %s and fecha<%s",('%'+evento+'%',fecha1,fecha2,) )
        df = pd.DataFrame(self.mycursor.fetchall())
        df.columns = self.mycursor.column_names
        return df
    def obtenerEventosPorFechaYSimbolo(self,fecha,symbol=str):
         
         divisa1=symbol.split("_")[0]
         divisa2=symbol.split("_")[1]
         self.mycursor.execute("select event,forecast,actual,previus,currency from calendario where fecha=%s and currency=%s union select event,forecast,actual,previus,currency  from calendario where fecha=%s and currency=%s",(fecha,divisa1,fecha,divisa2,))
         myresult=(self.mycursor.fetchall())
         resultados=[]
         for x in myresult:
            
             lista={}
             lista["event"]=x[0]
             lista["forecast"]=(x[1])
             lista["actual"]=(x[2])
             lista["previous"]=(x[3])
             lista["currency"]=x[4]
             resultados.append(lista)
         
         return resultados
    def obtenerCalendario(self):
           self.mycursor.execute("select * from calendario")
           df = pd.DataFrame(self.mycursor.fetchall())
           df.columns = self.mycursor.column_names
           return df
        
    def anadirCorrelacion(self,correlacion,symbol1=str,symbol2=str):
        today = dt.date.today()


        tiempo = today.strftime("%Y-%m-%d")
        self.mycursor.execute("INSERT INTO correlaciones VALUES(%s,%s,%s,%s)", (symbol1,symbol2,float(correlacion),tiempo))

        self.mydb.commit()
    def obtenerCorrelacion(self,symbol1,symbol2):
          self.mycursor.execute("select correlacion from correlaciones where simbolo1=%s and simbolo2=%s and tiempoDeInsercion >= all (select tiempoDeInsercion from correlaciones) union select correlacion from correlaciones where simbolo1=%s and simbolo2=%s and tiempoDeInsercion >= all (select tiempoDeInsercion from correlaciones)",(symbol1,symbol2,symbol2,symbol1,))
          myresult=(self.mycursor.fetchall())
          return myresult[0][0]
        
         