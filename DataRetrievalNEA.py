import requests
import json
DATE = "2022-10-09"
TIME = "14:12:13"
ploads = {"date_time":DATE + "T" + TIME}
urlDict={
    "Rainfall":"https://api.data.gov.sg/v1/environment/rainfall", 
    "Air Temperature":"https://api.data.gov.sg/v1/environment/air-temperature",
    "RH":"https://api.data.gov.sg/v1/environment/relative-humidity",
    "Wind Direction":"https://api.data.gov.sg/v1/environment/wind-direction",
    "Wind Speed":"https://api.data.gov.sg/v1/environment/wind-speed"
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
        
print("Input time: {} {}".format(DATE,TIME))
for key in urlDict:
    fetchAPI(key)