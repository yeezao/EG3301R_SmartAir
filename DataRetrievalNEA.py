import requests
import json

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
    readings = r.json()["items"][0]["readings"]
    timestamp = r.json()["items"][0]["timestamp"]
    res = ""
    for i in readings:
        if i["station_id"] == "S50":
            res = i["value"]
            break
    print("ResultTimestamp:{} {}:{} ".format(timestamp.split("T"),param,res))
    return str(param) + " : " + str(res) + unitDict[param] + ", "


# DATE=input()
# TIME=input()
# ploads = {"date_time":DATE + "T" + TIME}
ploads = {"date_time":input()}
print("Input time: {}".format(ploads))
output = ""
for key in urlDict:
    output+=fetchAPI(key)
print(output)