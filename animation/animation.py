# animated_line_plot.py

from random import randint
from tracemalloc import start

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import csv
from matplotlib.animation import FFMpegWriter
import pandas as pd


def readCSV (csvname):
    df=pd.read_csv(csvname)
    return df

def timeToSeconds(timestamp):
    tempArr=timestamp.split(":")
    return int(tempArr[0])*3600+int(tempArr[1])*60 + int(tempArr[2])

def makeArr(df,param):
    outputlist = []
    startTime = timeToSeconds(df["time"][0])
    numSensors = int(df["id"].max())
    for i in range (1,numSensors+1):
        tempdf =df.loc[df['id'] == float(i)][["time",param]]
        outputlist.append([tempdf["time"].apply(timeToSeconds).apply(lambda x : x- startTime).tolist(),tempdf[param].tolist()])
    return outputlist

def makeActionsArr(df):
    output = []
    startTime = timeToSeconds(df["time"][0])
    tempdf =df.loc[df['fan_action'] != ""][["time","fan_action"]]
    output.append([tempdf["time"].apply(timeToSeconds).apply(lambda x : x- startTime).tolist(),tempdf["fan_action"].tolist()])
    tempdf =df.loc[df['filter_action'] != ""][["time","filter_action"]]
    output.append([tempdf["time"].apply(timeToSeconds).apply(lambda x : x- startTime).tolist(),tempdf["filter_action"].tolist()])
    flag =1
    fanTimes = []
    for i in range(len(output[0][1])):
        if output[0][1][i]==flag:
            fanTimes.append([output[0][0][i]])
            flag = flag * -1
    filterTimes = []
    flag=1
    for i in range(len(output[1][1])):
        if output[1][1][i]==flag:
            filterTimes.append([output[1][0][i]])
            flag = flag * -1
    return [fanTimes,filterTimes]







#function that draws each frame of the animation takes in arrays to be plotted [[x1,y1],[x2,y2]] 
def animate(i,dataArr,actionsArr,param):
    ax.clear()
    for r in range (len(dataArr)):
        ax.plot(dataArr[r][0][:i],dataArr[r][1][:i] , label="sensor {}".format(r))
    flag1 = -1
    flag2 = -1
    for j in actionsArr[0]:
        if j[0]< dataArr[0][0][i]:
            if flag1==-1:
                ax.axvline(x = j[0], color = 'b', linestyle = "solid")
                flag1 = flag1 *-1
            else:
                ax.axvline(x = j[0], color = 'b', linestyle='dotted',)
                flag1 = flag1 *-1

    for k in actionsArr[1]:
        if k[0]< dataArr[0][0][i]:
            if flag2==-1:
                ax.axvline(x = k[0], color = 'r',linestyle = "dashdot")
                flag2=flag2*-1
            else:
                ax.axvline(x = k[0], color = 'r', linestyle='dotted')
                flag2 = flag2 *-1
    ax.set_xlim([0,max(dataArr[0][0])+30])
    ax.set_ylim([0,PARAM_THRESHOLDS[param]])

PARAM_THRESHOLDS = {"TVOC":3000, "CO2": 2000}

if __name__ == "__main__":
    print("Read from: ")
    readSheet=input()
    print("Read param: ")
    param = input()
    print ("Save to: ")
    f = r"./" + input() +".mp4"
    dataframe = readCSV(readSheet)
    dataArr = makeArr(dataframe, param)
    actionsArr = makeActionsArr(dataframe)
    fig, ax= plt.subplots()    
    ani = FuncAnimation(fig, animate, frames=len(dataArr[0][0]),fargs=[dataArr,actionsArr,param], interval=10, repeat=False)
    #ax.legend(loc='best')
    plt.show()
    ani.save(f, writer=animation.FFMpegWriter(fps=60) )
    plt.close()

#test    
# if __name__ == "__main__":
#     print("Read from: ")
#     readSheet="aq_readings (3).csv"
#     print("Read param: ")
#     param = "TVOC"
#     print ("Save to: ")
#     f = r"./" + "test" +".mp4"
#     dataframe = readCSV(readSheet)
#     dataArr = makeArr(dataframe, param)
#     actionsArr = makeActionsArr(dataframe)
#     print(actionsArr)
#     fig, ax= plt.subplots()    
#     ani = FuncAnimation(fig, animate, frames=len(dataArr[0][0]),fargs=[dataArr,actionsArr], interval=1, repeat=False)
#     plt.show()
#     ani.save(f, writer=animation.FFMpegWriter(fps=60) )
#     plt.close()




#save ani to gif
# writergif = animation.PillowWriter(fps=30) 
# ani.save(f, writer=writergif)
