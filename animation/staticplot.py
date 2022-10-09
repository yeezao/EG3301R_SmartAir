# animated_line_plot.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
from datetime import datetime
import pandas as pd
import matplotlib.dates as mdates
import math

#reads csv to dataframe with timestamp formatted
def readCSV (csvname):
    df=pd.read_csv(csvname)
    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"],dayfirst=True)
    return df

#creates dictionary of sensor dataframes based on id, and actions tuple of timestamps of action sign changes 
def createPlotData(df):
    uniqueSensors = df["id"].unique()
    resultDict = {}
    for i in uniqueSensors:
        if not math.isnan(i):
            tempdf = df.loc[df['id'] == i]
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
        ax.plot(sensorDict[key]["timestamp"],sensorDict[key][param],label="sensor {}".format(key))
    for i in range(len(actionArr)):
        for j in range(len(actionArr[i][0])):
            print(i)
            ax.axvline(x = actionArr[i][0][j], color = ('r' if i==0 else 'g' ), linestyle = ("dotted" if actionArr[i][1][j] == -1 else "solid") )
            
    ax.set_xlabel("Time")
    ax.set_title(param + " against  time")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('(%d) %H:%M:%S'))
    legend=ax.legend()
    #ax.set_xlim([0,max(sensorDict[key]["timestamp"])+30])
    ax.set_ylim([0,PARAM_AXES_LIM[param]])
    


    
PARAMS = ["timestamp", "TVOC","CO2"]
PARAM_AXES_LIM = {"TVOC":2000, "CO2": 4000, "PM1":20,"PM2.5":300,"PM10":20,"Temp":35,"Humidity":100}

if __name__ == "__main__":
    readSheet="aq_readings_0810_05.csv"
    param = "CO2"
    dataframe = readCSV(readSheet)
    fig,ax=plt.subplots()
    sensorDict, actionArr = createPlotData(dataframe)
    #print (actionArr[0][0][0].month)

    #print(sensorDict)
    makePlot(sensorDict,actionArr, ax,param)
    print(dataframe)
    #ax.format_xdata = mdates.DateFormatter('%H:%M:%S')
    plt.show()
    plt.close()