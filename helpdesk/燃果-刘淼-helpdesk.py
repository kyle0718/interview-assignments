# -*- coding:UTF-8 -*-
# Env:python3.6
# Writer: Liu Miao

import re
import json
import requests


name = locals()
jsonList = []

fileName = open('./Helpdesk_interview_data_set','r',encoding='utf-8')
errorFile = []

for line in fileName:
    if 'error' in line:
        errorFile.append(line)

for i in range(0,24):
    hour = ("%02d" % i)
    name[str(hour)] = []

for line in errorFile:
    timeTmpStrTmp = re.search('\d{2}:\d{2}:\d{2}',str(line)).group().split(':',1)
    timeWindow = timeTmpStrTmp[0]
    name[str(timeWindow)].append(timeWindow)
    numberOfOccurrence = len(name[str(timeWindow)])

    lineTmpStrTmp = re.sub('\w{3} \d{2} \d{2}:\d{2}:\d{2}','',str(line))
    lineTmpStr = lineTmpStrTmp.split(':',1)

    description = lineTmpStr[1]
    lineTmpStr1 = lineTmpStr[0].strip(' ').split(' ',1)
    deviceName = lineTmpStr1[0]
    processName = lineTmpStr1[1].split('[',1)[0]

    processId = re.search('(\d+)',lineTmpStr1[1]).group(0)
    dict = {'deviceName':deviceName,
            'processId':processId,
            'processName':processName,
            'description':description,
            'timeWindow':timeWindow,
            'numberOfOccurrence':numberOfOccurrence,
    }
    jsonList.append(dict)

jsonArr = json.dumps(jsonList, ensure_ascii=False)

url = 'https://foo.com/bar'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
response = requests.post(url,data=jsonArr,headers=headers,verify=False)
print(response)
