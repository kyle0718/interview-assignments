# -*- coding:UTF-8 -*-
# Env:python3.6
# Writer: Liu Miao   mail:kyle0718@gmail.com
# Cmd: python3.6 script.py /path/file.gz
# Note: Microsoft OS System Path exp("c:/path/file" or "c:\\path\\file")

import re,json,requests,gzip
import sys,traceback,logging,time

logging.basicConfig(filename='script.log', level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

gzFile = sys.argv[1]
name = locals()
jsonList = []
errorFile = []

def un_gz(gzFile):
    fileName = gzFile.replace(".gz", "")
    fileGz = gzip.GzipFile(gzFile)
    open(fileName, "wb+").write(fileGz.read())
    fileGz.close()
    return fileName

def format_data(line):
    timeTmpStrTmp = re.search('\d{2}:\d{2}:\d{2}', str(line)).group().split(':', 1)
    timeWindow = timeTmpStrTmp[0]
    name[str(timeWindow)].append(timeWindow)
    numberOfOccurrence = len(name[str(timeWindow)])

    lineTmpStrTmp = re.sub('\w{3} \d{2} \d{2}:\d{2}:\d{2}', '', str(line))
    lineTmpStr = lineTmpStrTmp.split(':', 1)

    description = lineTmpStr[1]
    lineTmpStr1 = lineTmpStr[0].strip(' ').split(' ', 1)
    deviceName = lineTmpStr1[0]
    processName = lineTmpStr1[1].split('[', 1)[0]

    processId = re.search('(\d+)', lineTmpStr1[1]).group(0)
    dict = {'deviceName': deviceName,
            'processId': processId,
            'processName': processName,
            'description': description,
            'timeWindow': timeWindow,
            'numberOfOccurrence': numberOfOccurrence,
            }
    jsonList.append(dict)

if __name__ == '__main__':
    try:
        for i in range(0, 24):
            hour = ("%02d" % i)
            name[str(hour)] = []

        errFileName = open(un_gz(gzFile),'r',encoding='utf-8')

        for line in errFileName:
            if 'error' in line:
                format_data(line)

        jsonArr = json.dumps(jsonList, ensure_ascii=False)
        url = 'https://foo.com/bar'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        requests.post(url, data=jsonArr, headers=headers, verify=False)

        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        file = open('./jsonData.log', 'a', encoding='utf-8')
        file.write(end_time + '\n' + "  " + jsonArr  + '\n')
        file.close()

    except:
        logging.debug(traceback.format_exc())