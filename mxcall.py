import logging
import getopt
import sys
import requests
import json
from termcolor import colored

apiKey = ''     #insert your API key here
commands = []   #write into the txt file, not here
domains = []    #write into the txt file, not here
selector = ""   #insert the DKIM selector here

#LOGGER CONFIG
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_log = logging.FileHandler('mxapi.log')
file_log.setLevel(logging.DEBUG)
console_log = logging.StreamHandler()
console_log.setLevel(logging.INFO)
file_format = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)s:%(levelname)-8s %(message)s')
console_format = logging.Formatter('[%(asctime)s] %(levelname)-8s - %(message)s')
file_log.setFormatter(file_format)
console_log.setFormatter(console_format)
logger.addHandler(file_log)
logger.addHandler(console_log)

def query_api(logger, apikey, command, domain, selector):

    logger.debug('Entering query_api')
    
    url = 'https://mxtoolbox.com/api/v1/Lookup/' + command + "/"+ domain
    if(command == "DKIM"):
        if(selector == ""):
            selector = "google" #default selector
        url = 'https://mxtoolbox.com/api/v1/Lookup/' + command + "/"+ "?argument=" + domain + ":" + selector
    headers = {'Authorization': apikey}
    logger.debug('Trying api request for '+ domain + 'with '+command)
    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        raise
    logger.debug('Finished making api request')
    data = r.text
    return data


with open('domains.txt') as f:
    domains = f.read().splitlines()
    
with open('commands.txt') as f:
    commands = f.read().splitlines()

file = open("result.txt","w")

for d in domains:
    print('\033[95m'+d + "\033[0m")
    file.write("----------------------------------"+ "\n")
    file.write(d+ "\n")
    file.write("----------------------------------"+ "\n")
    s = selector
    for c in commands:
        data = query_api(logger,apiKey,c,d,s)
        resp_dict = json.loads(data)
        print('\033[1m'+c + "\033[0m")
        file.write(c+ "\n")
        file.write("Failure:"+ "\n")
        for p in resp_dict['Failed']:
            print('\033[91m'+ p['Name'] +": "+ p['Info'] + '\033[0m')
            file.write(p['Name'] +": "+ p['Info']+ "\n")
        file.write("Warnings:"+ "\n")
        for p in resp_dict['Warnings']:
            print('\033[93m'+ p['Name'] +": "+ p['Info'] + '\033[0m')
            file.write(p['Name'] +": "+ p['Info']+ "\n")
        for p in resp_dict['Passed']:
            print('\033[92m'+p['Name'] +": "+ p['Info'] + '\033[0m')
        for p in resp_dict['Information']:
            print(json.dumps(p))

        print("-------------------------")

file.close()