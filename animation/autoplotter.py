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

#takes in sensor dictionary of dataframes, actions tuple ([[],[]],[[],[]]), ax object and param to plot
def makePlot(sensorDict,actionArr, ax,param):
    for key in sensorDict:
        ax.plot((sensorDict[key]["timestamp"]),sensorDict[key][param],label="sensor {}".format(key))
    for i in range(len(actionArr)):
        for j in range(len(actionArr[i][0])):
            ax.axvline(x = actionArr[i][0][j], color = ('b' if i==0 else 'g' ), linestyle = ("dotted" if actionArr[i][1][j] == -1 else "solid") )
    ax.set_xlabel("Time")
    ax.set_title(param + " against  time")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('(%d) %H:%M:%S'))
    legend=ax.legend()
    #ax.set_xlim([0,max(sensorDict[key]["timestamp"])+30])
    ax.set_ylim([0,PARAM_AXES_LIM[param]])

def windowPlot(sensorDict,actionArr,ax,param,start,end):
    print("{} Statistics for the period {} to {}".format(param,start,end))
    for key in sensorDict:
        sensordf = sensorDict[key]
        ax.plot((sensorDict[key]["timestamp"]),sensorDict[key][param],label="sensor {}".format(key))
        sensordfranged = sensordf[(sensordf['timestamp'] >= start) & (sensordf['timestamp'] <= end)]
        print("Sensor {}".format(key))
        print ("mean: " + str(sensordfranged[param].mean()))
        print ("std: " + str(sensordfranged[param].std()))
        print ("max: " + str(sensordfranged[param].max()))
        print ("min: " + str(sensordfranged[param].min()))
        print ("range: " + str(sensordfranged[param].max()-sensordfranged[param].min()))
        print("------------------------------------")
    for i in range(len(actionArr)):
        for j in range(len(actionArr[i][0])):
            ax.axvline(x = actionArr[i][0][j], color = ('b' if i==0 else 'g' ), linestyle = ("dotted" if actionArr[i][1][j] == -1 else "solid") )       
    ax.axvline(x = start, color = ('r' ), linestyle = ("solid") )       
    ax.axvline(x = end, color = ('r' ), linestyle = ("solid") )       
    ax.set_xlabel("Time")
    ax.set_title(param + " against  time")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('(%d)%H:%M'))
    legend=ax.legend()
    ax.set_xlim([start,end])
    if (param == "PMV"):
        ax.set_ylim([-PARAM_AXES_LIM[param],PARAM_AXES_LIM[param]])    
    else:
        ax.set_ylim([0,PARAM_AXES_LIM[param]])
    

def rollingAveragedGradientPlot(sensorDict,actionArr,ax,param):
    sampling = 300
    for key in sensorDict:
        result = sensorDict[key][param].rolling(sampling).apply(lambda y:np.polyfit(range(len(y)), y, 1)[0] )
        print(type(result))
        ax.plot((sensorDict[key]["timestamp"]),result,label="sensor {}".format(key))
    for i in range(len(actionArr)):
        for j in range(len(actionArr[i][0])):
            ax.axvline(x = actionArr[i][0][j], color = ('b' if i==0 else 'g' ), linestyle = ("dotted" if actionArr[i][1][j] == -1 else "solid") )  
    ax.axhline(y = 0, color = ('black' ), linestyle = ("solid") )  
    ax.set_xlabel("Time")
    ax.set_title("Rolling {} sample {} gradient against time".format(sampling,param))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('(%d) %H:%M:%S'))
    legend=ax.legend()
    return

def timeToClear(inputTuple):
    startIndex = -1
    endIndex = -1
    for i in range(len(inputTuple[1])):
        if inputTuple[0][1][i]==1.0:
            startIndex = i
            break
    for j in range(len(inputTuple[1])-1,0,-1):
        if inputTuple[0][1][j]==-1.0:
            endIndex = j
            break
    print("First on " + str(inputTuple[0][0][startIndex]))
    print("Last off " + str(inputTuple[0][0][endIndex]))
    return inputTuple[0][0][endIndex]-inputTuple[0][0][startIndex]

PARAMS = ["TVOC","CO2","PM1","PM2.5","PM10","Temp","Humidity","PMV"]
PARAM_AXES_LIM = {"TVOC":200, "CO2": 1500, "PM1":20,"PM2.5":50,"PM10":20,"Temp":35,"Humidity":100,"PMV":2}
functions = {"p":makePlot, "w":windowPlot,"g":rollingAveragedGradientPlot,"time":timeToClear}
PHASES = {"1_start":"13 10/10","1_end":"13 25/10",
          "2_start":"13 25/10","2_end":"15 28/10",
          "3_start":"15 28/10","3_end":"14 31/10",
          "4_start":"14 31/10","4_end":"13 1/11",
          "5_start":"13 1/11","5_end":"17 2/11",
          "6_start":"17 2/11","6_end":"12 4/11",
          }

#enter sheet and time window
#eg. python autoplotter.py baseline1.csv 13 11/10 10 25/10
'''
if __name__ == "__main__":
    readSheet = sys.argv[1]
    startstr = PHASES[sys.argv[2]]+"/22"
    endstr = PHASES[sys.argv[3]]+"/22"
    start = datetime.strptime(startstr, '%H %d/%m/%y')
    end = datetime.strptime(endstr, '%H %d/%m/%y')
    func = "w"
    dataframe = readCSV(readSheet)
    sensorDict, actionArr = createPlotData(dataframe)
    for i in PARAMS:
        print("READING {} =======================================".format(i))
        fig,ax=plt.subplots()
        functions[func](sensorDict,actionArr,ax,i,start,end)
        plt.savefig('graphs/{}_{}_{}.png'.format(i,start.strftime("%H%M_%d%m%Y"),end.strftime("%H%M_%d%m%Y")))
        plt.close()
'''
if __name__ == "__main__":
    readSheet = sys.argv[1]
    dataframe = readCSV(readSheet)
    sensorDict, actionArr = createPlotData(dataframe)
    func = "w"
    for i in PARAMS:
        print("READING {} =======================================".format(i))
        for j in range(1,5):
            print("PHASE {} ===============".format(j))
            startstr = PHASES["{}_start".format(j)]+"/22"
            endstr = PHASES["{}_end".format(j)]+"/22"
            start = datetime.strptime(startstr, '%H %d/%m/%y')
            end = datetime.strptime(endstr, '%H %d/%m/%y')
            fig,ax=plt.subplots()
            functions[func](sensorDict,actionArr,ax,i,start,end)
            plt.savefig('graphs/{}_phase{}_{}_{}.png'.format(i,j,start.strftime("%H_%d%m"),end.strftime("%H_%d%m")))
            plt.close()
        
        
