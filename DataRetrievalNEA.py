import requests
import json
from statistics import mean 


urlDict={
    "Air Temperature":"https://api.data.gov.sg/v1/environment/air-temperature",
    "RH":"https://api.data.gov.sg/v1/environment/relative-humidity",
    "Wind Speed":"https://api.data.gov.sg/v1/environment/wind-speed",
    "Wind Direction":"https://api.data.gov.sg/v1/environment/wind-direction",
    "Rainfall":"https://api.data.gov.sg/v1/environment/rainfall"
}

unitDict={
    "Air Temperature":"C",
    "RH":"%",
    "Wind Speed":"km/h",
    "Wind Direction":"",
    "Rainfall":""
}


def fetchAPI(param):
    r = requests.get(urlDict[param],params=ploads)
    items = r.json()["items"]
    timestamp = r.json()["items"][0]["timestamp"]
    res = []
    for readings in items:
        for value in readings["readings"]:
            if value["station_id"] == "S50":
                res.append(value["value"])
                break
    #print("ResultTimestamp:{} {}:{} ".format(timestamp.split("T"),param,res))
    x = mean(res)
    return x


# DATE=input()
# TIME=input()
# ploads = {"date_time":YYYY-MM-DD[T]HH:mm:ss}
# ploads = {"date":input()}
# print("Input time: {}".format(ploads))
# output = ""
# for key in urlDict:
#     output+=fetchAPI(key)
# print(output)

date = input()
for i in range (3):
    ploads = {"date":date}
    print("Input time: {}".format(ploads))
    output=fetchAPI("Air Temperature")
    print(output)
    date = date[:-1] + str(int(date[-1]) + 1)