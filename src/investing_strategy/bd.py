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
USER="usuario1"
PASSWORD="password"
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
        
 
    def addCalendar(self,id,date,zone,currency,importance,event,actual,forecast,previous):
        f = '%Y-%m-%d %H:%M:%S'
        tupla = (id, date, zone,currency,importance,event,actual,forecast,previous)
        cadena = "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"


        self.mycursor.execute("INSERT INTO calendario VALUES" + cadena, tupla)
        self.mydb.commit()

    
    def getCalendar(self,evento:str,fecha1:str,fecha2:str,simbolo:str):
        

        self.mycursor.execute("select * from calendario where event like %s and fecha>= %s and fecha<%s and currency=%s and importance='high' order by fecha asc ",(str("%")+evento+str("%"),fecha1,fecha2,simbolo) )
        df = pd.DataFrame(self.mycursor.fetchall())
        if len(df)==0:
             self.mycursor.execute("select * from calendario where event like %s and fecha>= %s and fecha<%s and currency=%s and importance='medium' order by fecha asc ",(str("%")+evento+str("%"),fecha1,fecha2,simbolo) )
             df = pd.DataFrame(self.mycursor.fetchall())
            
        df.columns = self.mycursor.column_names
        print("symbol: %s, number of events: %s"%(simbolo,len(df)))
        return df
    
    
    def getCalendarUniqueValues(self,evento:str,fecha1:str,fecha2:str,simbolo:str):
        

        self.mycursor.execute("select * from calendario ca where event like %s and fecha>= %s and fecha<%s and currency=%s and importance='high' and fecha>=all(select fecha from calendario c where event like %s and fecha>= %s and fecha<%s and currency=%s and importance='high' and MONTH(ca.fecha)=MONTH(c.fecha) and  YEAR(ca.fecha)=YEAR(c.fecha))   order by fecha asc ",(str("%")+evento+str("%"),fecha1,fecha2,simbolo,str("%")+evento+str("%"),fecha1,fecha2,simbolo) )
        df = pd.DataFrame(self.mycursor.fetchall())
        if len(df)==0:
             self.mycursor.execute("select * from calendario ca where event like %s and fecha>= %s and fecha<%s and currency=%s and importance='medium' and fecha>=all(select fecha from calendario c where event like %s and fecha>= %s and fecha<%s and currency=%s and importance='medium' and MONTH(ca.fecha)=MONTH(c.fecha) and  YEAR(ca.fecha)=YEAR(c.fecha))   order by fecha asc ",(str("%")+evento+str("%"),fecha1,fecha2,simbolo,str("%")+evento+str("%"),fecha1,fecha2,simbolo) )
             df = pd.DataFrame(self.mycursor.fetchall())
            
        df.columns = self.mycursor.column_names
        print("symbol: %s, number of events: %s"%(simbolo,len(df)))
        return df
   
   
        
         
