# animated_line_plot.py
from math import nan
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from matplotlib import animation
import pandas as pd
import math


def readCSV (csvname):
    df=pd.read_csv(csvname)
    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"])
    return df

def getSignChanges(df):
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
    return actionArr

def animate(i):
    dataframe = readCSV(readSheet)
    ax.cla()
    for j in dataframe["id"].unique():
        if not math.isnan(j):
            ax.plot(dataframe.loc[dataframe['id'] == j]["timestamp"],dataframe.loc[dataframe['id'] == j][param],label="sensor {}".format(j))
    actionArr = getSignChanges(dataframe)
    for k in range(len(actionArr)):
        for l in range(len(actionArr[k][0])):
            ax.axvline(x = actionArr[k][0][l], color = ('r' if k==0 else 'g' ), linestyle = ("dotted" if actionArr[k][1][l] == -1 else "solid") )
     
    ax.set_xlabel("Time")
    ax.set_title(param + " against  time")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('(%d) %H:%M:%S'))
    legend=ax.legend()
    ax.set_xlim(min(dataframe["timestamp"]),max(dataframe["timestamp"]))
    ax.set_ylim([0,PARAM_AXES_LIM[param]])
    

PARAM_AXES_LIM = {"TVOC":3000, "CO2": 2000}
INTERVAL = 100

if __name__ == "__main__":
    readSheet = sys.argv[1]
    param = sys.argv[2]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)    
    ani = FuncAnimation(plt.gcf(), animate, interval=INTERVAL)
    plt.show()
    plt.close()


