from http.client import HTTPSConnection
from json.decoder import JSONDecodeError
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from multiprocessing.dummy import Pool as ThreadPool
import datetime
import pandas as pd






def get_tags ():
    url = "https://palermo.viper.comcast.net/api/tags"

    payload={}
    headers = {}

    r = requests.request("GET", url, headers=headers, data=payload)
    jsonData = r.json()

    #print(jsonData)
    for t in jsonData:
        if t["key"] == "division" and t['value'] == "central":
            cdTag = t['id']
            return cdTag
            
    
def get_ccvs (cdTag):
        
    url = f"https://palermo.viper.comcast.net/api/ccvs?tagIds={cdTag}"

    payload={}
    headers = {}

    r = requests.request("GET", url, headers=headers, data=payload)
    jsonData = r.json()
    #print(jsonData)
    ccvList = []
    for c in jsonData:
        if c['tagged']['value']['supports551'] == False:
            ccvList.append(c['tagged']['value']['id'])
    #print (len(ccvList), ccvList)
    return ccvList


def get_ccv_detail (ccvList):
    qpskList = []
    for c in ccvList:
            
        url = "https://palermo.viper.comcast.net/api/ccv/" + c 

        payload={}
        headers = {}

        r = requests.request("GET", url, headers=headers, data=payload)
        jsonData = r.json()
        print ()
        print(jsonData['name']['hubCode'] + str(jsonData['name']['ccvNumber']))
        ccvName = jsonData['name']['hubCode'] + str(jsonData['name']['ccvNumber'])
        
        if jsonData['ciscoCasSystem']:
            for e in jsonData['ciscoCasSystem']['oob552Engines'] :
                qpsk = {}
                name = str(e['name'])
                nameSplit = name.split()
                
                ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', name )
                if ip:
                    qpsk['ccv'] = ccvName
                    qpsk['qpskName'] = nameSplit[0]
                    qpsk['qpskIp'] = ip[0]
                    qpskList.append(qpsk)
        # print()
        # print("QPSK LIST")
        # print(qpskList)
        # print()
    return qpskList






def get_rpd_data (q):
    get_rpd_status (q)
    get_rpd_config_network (q)
    print()
    

def get_rpd_status (q):
    ip = q['qpskIp']    
    url = f"https://{ip}/views/Status_RPD_Status"
    #print (url)

    payload={}
    headers = {
    'Authorization': 'Basic RDk0ODVfYWRtaW46UXBzazJuM3c='
    }
    try:
        r = requests.request("GET", url, headers=headers, data=payload, verify=False, timeout=20)
        jsonData = r.json()
        #print(jsonData['widgets'][0]['values'][0])
        q.update(jsonData['widgets'][0]['values'][0])
        #print(q)
    except requests.exceptions.ConnectionError:
        print(q['qpskIp']," Status Connection Error")  
    except JSONDecodeError:
        print(q['qpskIp']," JSON decode error") 

def get_rpd_config_network (q):
    ip = q['qpskIp']
    url = f"https://{ip}/views/Configuration_Network"

    payload={}
    headers = {
    'Authorization': 'Basic RDk0ODVfYWRtaW46UXBzazJuM3c='
    }
    try:
        r = requests.request("GET", url, headers=headers, data=payload, verify=False, timeout=3)
        jsonData = r.json()
        q.update(jsonData['widgets'][0]['values'][0])
        q.update(jsonData['widgets'][2]['values'][0])
        print(q)
    except requests.exceptions.ConnectionError:
        print(f"{q['qpskIp']} Network Connection Error")  
    except JSONDecodeError:
        print(f"{q['qpskIp']} JSON decode error") 
    except requests.exceptions.RequestException:
        print(f"{q['qpskIp']} Timeout error") 


startTime = datetime.datetime.now()
cdTag = get_tags ()
print(f"cdTag = {cdTag}")
ccvList = get_ccvs (cdTag)
qpskList = get_ccv_detail (ccvList)
print("original QPSK List")
print(qpskList)
print()

# Make the Pool of workers
pool = ThreadPool(9)


pool.map(get_rpd_data, qpskList)
# Open the urls in their own threads
# and return the results
#close the pool and wait for the work to finish
pool.close()
pool.join() 

#get_rpd_data (qpskList)
print(qpskList)

qpsk_frame = pd.DataFrame(qpskList)
print(qpsk_frame.info())
qpsk_gateways = qpsk_frame['Default Gateway'].unique
qpsk_gateways
fileDate = datetime.datetime.now().strftime("%Y_%m_%d_%I-%M-%S_%p")
saveFileName = f"c:\\xfer\\qpsk_frame_{fileDate}.xlsx"
writer = pd.ExcelWriter(saveFileName, engine='xlsxwriter')                
qpsk_frame.to_excel(writer, index=False, sheet_name="qpsk_data")
writer.book.close()
finishTime = datetime.datetime.now()
print(f"runtime = {finishTime - startTime}")
