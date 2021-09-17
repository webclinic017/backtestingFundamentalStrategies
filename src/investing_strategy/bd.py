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
        

        self.mycursor.execute("select * from calendario where event like %s and fecha>= %s and fecha<%s and currency=%s and importance='high' ",(str("%")+evento+str("%"),fecha1,fecha2,simbolo) )
        df = pd.DataFrame(self.mycursor.fetchall())
        if len(df)==0:
             self.mycursor.execute("select * from calendario where event like %s and fecha>= %s and fecha<%s and currency=%s and importance='medium' ",(str("%")+evento+str("%"),fecha1,fecha2,simbolo) )
             df = pd.DataFrame(self.mycursor.fetchall())
            
        df.columns = self.mycursor.column_names
        print("symbol: %s, number of events: %s"%(simbolo,len(df)))
        return df
   
        
         
