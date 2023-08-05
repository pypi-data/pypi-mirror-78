import json
import requests
import time

def getdict(url):
    p = requests.get(url)
    res_p = p.content.decode()
    return json.loads(res_p)

def gettime(timeStamp,style="%Y--%m--%d %H:%M:%S"):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime(style, timeArray)
    return otherStyleTime
