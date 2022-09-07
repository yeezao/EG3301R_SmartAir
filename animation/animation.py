# animated_line_plot.py

from random import randint
from tracemalloc import start

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import csv
from matplotlib.animation import FFMpegWriter


co2 =[]
voc =[]
time=[]
paramDict={"co2":co2,"voc":voc}

#sunday csv format read
def readAQ (csvname):
    with open(csvname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        startstamp=0
        for row in csv_reader:
            if line_count == 0: #dont read first line
                line_count += 1
            elif line_count % 2 == 0: #dont read blank lines
                line_count +=1
            else:
                if line_count==1: #initialise start time
                    timestamp=0
                    startstamp=process(row[1])
                    time.append(startstamp)
                else:
                    time.append(process(row[1])-startstamp)

                co2.append(float(row[4]))
                voc.append(float(row[5]))
                line_count += 1

#normal csv format read
def readAQ1 (csvname):
    with open(csvname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        startstamp=0
        for row in csv_reader:
            if line_count == 0: #dont read first line
                line_count += 1
            else:
                if line_count==1: #initialise start time
                    timestamp=0
                    startstamp=process(row[1])
                    time.append(0)
                else:
                    time.append(process(row[1])-startstamp)

                co2.append(float(row[4]))
                voc.append(float(row[5]))
                line_count += 1

def process(timestamp):
    tempArr=timestamp.split(":")
    return int(tempArr[0])*3600+int(tempArr[1])*60 + int(tempArr[2])


# create the figure and axes objects
fig, ax = plt.subplots()

#function that draws each frame of the animation
def animate(i,yArr):
    ax.clear()
    ax.plot(time[0:i], yArr[0:i])
    ax.set_xlim([0,max(time)+30])
    ax.set_ylim([0,5000])


# def animate(i):
#     ax.clear()
#     ax.plot(time[0:i], co2[0:i])
#     ax.set_xlim([0,830])
#     ax.set_ylim([0,2050])

#readSheet="aq_readings_300822_s42.csv"
#toMeasure=[voc]
#f = r"c://Users/liewy/Desktop/animation/s4_2voc.mp4"
# toMeasure=[co2]
# f = r"c://Users/liewy/Desktop/animation/s4_2co2.mp4"
if __name__ == "__main__":
    print("Read from: ")
    readSheet=input()
    print("Read param: ")
    toMeasure = [paramDict[input()]]
    print ("Save to: ")
    f = r"./" + input() +".mp4"
    readAQ1(readSheet)
    print(time)
    print(toMeasure)
    print("Time points: "+str(len(time)))
    print("VOC points: "+str(len(voc)))
    print("CO2 points: "+str(len(co2)))
    print("Last VOC point: "+str(voc[-1]))
    print("Last CO2 point: "+str(co2[-1]))
    print("Last Time point: "+str(time[-1]))

    # run the animation
    ani = FuncAnimation(fig, animate, frames=len(time),fargs=toMeasure,interval=100, repeat=False)
    plt.show()
    writervideo = animation.FFMpegWriter(fps=60) 
    ani.save(f, writer=writervideo)
    plt.close()
#save ani
# writergif = animation.PillowWriter(fps=30) 
# ani.save(f, writer=writergif)


