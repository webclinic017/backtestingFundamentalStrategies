import v20
import pandas as pd
import funcionesAnalisisEstacionaridad as aE
import datetime as dt
import numpy as np
import operator
import sys
import math
sys.path.append("./")
VARIANZAS=["var_2","var_4","var_6","var_8","var_10"]
lags= [2, 4, 6, 8, 10, 15, 20, 30, 40, 50, 100, 200, 500, 1000]
periodicidad="H1"
atrasos=[]
atrasos.append("media")
NOMBRE_ARCHIVO="divisasSpreadH1"
RUTA_ARCHIVO_SPREADS="../data/"+NOMBRE_ARCHIVO+"/"

for i in lags:
            atrasos.append("var_"+str(i))
atrasos.append("H")


atrasos.append("fuller")
atrasos.append("fullerEstimacion")
atrasos.append("desde")
atrasos.append("hasta")
        
        

dataframe=pd.DataFrame(columns=["fecha1","fecha2","symbol","half_life"])
def analizarEstacionaridad(fechas,symbols,valorMaximoHurst=0.5,valorMaximoFuller=0.1):
        
    for i in range(len(fechas)-1):
            
   
        
        res=pd.DataFrame(columns=atrasos)
        FECHA1=fechas[i]
        FECHA2=fechas[i+1]
        
        
        
        
        
        
        
     
        print("Fecha inicial:%s, que es dia de la semana %s"%(FECHA1,dt.datetime.strptime(FECHA1,"%Y-%m-%d").weekday()))
        print("Fecha inicial:%s, que es dia de la semana %s"% (FECHA2, dt.datetime.strptime(FECHA2, "%Y-%m-%d").weekday()))
    
    
        for symbol in symbols:
            #print("Simbolo -> %s" % symbol)
            prize_df = pd.read_csv(RUTA_ARCHIVO_SPREADS + symbol + ".csv")
            try:
                prize_df["time"]= pd.to_datetime(prize_df['time'])
                prize_df = prize_df.loc[operator.__and__(prize_df.loc[:, "time"] >= dt.datetime.strptime(FECHA1,"%Y-%m-%d"), prize_df.loc[:, "time"] <=  dt.datetime.strptime(FECHA2,"%Y-%m-%d"),)]
                print("Numero de entradas %s" % len(prize_df))
                resultados, u = aE.devolverResultados(prize_df["close"], lags)
                desde = prize_df.iloc[0, 0]
                hasta = prize_df.iloc[len(prize_df) - 1, 0]
    
                u.append(FECHA1)
                u.append(FECHA2)
                res.loc[symbol] = u
                
                if res.loc[symbol,"H"]<valorMaximoHurst and res.loc[symbol,"fuller"]<=valorMaximoFuller:
                    half_life=math.log(2)/(float(res.loc[symbol,"fullerEstimacion"]))
                    print("Symbol %s, hurst %s, fuller %s, half_life %s"%(symbol,res.loc[symbol,"H"],res.loc[symbol,"fuller"],half_life))
                    dataframe.loc[len(dataframe)]=[FECHA1,FECHA2,symbol,half_life]
            except Exception as e:
                print(e)
    
        
    return dataframe
      
