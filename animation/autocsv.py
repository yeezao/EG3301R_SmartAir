# animated_line_plot.py

import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
from datetime import datetime,timedelta
import pandas as pd
import matplotlib.dates as mdates
import math
import numpy as np
import csv


#reads csv to dataframe with timestamp formatted
def readCSV (csvname):
    df=pd.read_csv(csvname)
    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"],dayfirst=True).map(lambda x:x+timedelta(hours=18))
    return df

#creates dictionary of sensor dataframes based on id, and actions tuple of timestamps of action sign changes 
def createPlotData(df):
    uniqueSensors = df["id"].unique()
    resultDict = {}
    for i in uniqueSensors:
        if not math.isnan(i):
            tempdf = df.loc[df['id'] == i]
            tempdf["PMV"] = df.apply(lambda itt:-8.405 + 0.322 * itt.Temp -0.686 * 0.2, axis=1)
            resultDict[i] = tempdf
    tempdf = df[df['id'].isna()]
    fanArr=([],[])
    filterArr=([],[])
    fanState = 3
    filterState = 3
    for j in tempdf.index:
        if tempdf["fan_action"][j] != fanState and tempdf["fan_action"][j] != 0:
                fanArr[0].append(tempdf["timestamp"][j])
                fanState = tempdf["fan_action"][j]
                fanArr[1].append(tempdf["fan_action"][j])
    for k in tempdf.index:
        if tempdf["filter_action"][k] != filterState and tempdf["filter_action"][k]!=0:
            filterArr[0].append(tempdf["timestamp"][k])
            filterState = tempdf["filter_action"][k]
            filterArr[1].append(tempdf["filter_action"][k])
    actionArr = (fanArr,filterArr)
    return resultDict , actionArr


def windowPlot(sensorDict,actionArr,param,phase):
    startstr = PHASES["{}_start".format(phase)]+"/22"
    endstr = PHASES["{}_end".format(phase)]+"/22"
    start = datetime.strptime(startstr, '%H %d/%m/%y')
    end = datetime.strptime(endstr, '%H %d/%m/%y')
    temp = [param,phase]
    for key in sensorDict:
        sensordf = sensorDict[key]
        sensordfranged = sensordf[(sensordf['timestamp'] >= start) & (sensordf['timestamp'] <= end)]
        print(sensordfranged)
        temp.append (key)
        temp.append (round(sensordfranged[param].mean(),2))
        temp.append (round(sensordfranged[param].std(),2))
        temp.append (round((sensordfranged[param].max()-sensordfranged[param].min()),2))
    return temp

PARAMS = ["TVOC","CO2","PM1","PM2.5","PM10","Temp","Humidity","PMV"]
PARAM_AXES_LIM = {"TVOC":200, "CO2": 1500, "PM1":20,"PM2.5":50,"PM10":20,"Temp":35,"Humidity":100,"PMV":2}
PHASES = {"1_start":"13 10/10","1_end":"13 25/10",
          "2_start":"13 25/10","2_end":"15 28/10",
          "3_start":"15 28/10","3_end":"14 31/10",
          "4_start":"14 31/10","4_end":"13 1/11",
          "5_start":"13 1/11","5_end":"17 2/11",
          "6_start":"17 2/11","6_end":"12 4/11",
          }
NUM_PHASES = len(PHASES)//2

if __name__ == "__main__":
    readSheet = sys.argv[1]
    dataframe = readCSV(readSheet)
    sensorDict, actionArr = createPlotData(dataframe)
    #for each param
    yee = []
    # for i in PARAMS: 
    #     #for each phase
    #     for j in range(1, NUM_PHASES+1):            
    #         yee.append(windowPlot(sensorDict,actionArr,i,j))
    # with open("stats_file.csv","w+",newline='') as my_csv:
    #     csvWriter = csv.writer(my_csv,delimiter=',')
    #     csvWriter.writerow(["Param","Phase","id","mean","std","range","id","mean","std","range","id","mean","std","range","id","mean","std","range"])
    #     csvWriter.writerows(yee)
    
    print(windowPlot(sensorDict,actionArr,"CO2",1))
        
        
