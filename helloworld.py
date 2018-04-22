#!/usr/bin/python
#Python 2.7.6
#RestfulClient.py

import argparse
from xml.etree import ElementTree
import yaml
import json
import requests

req = requests.get("http://www.google.com")
print 'res', req.status_code

dockersecret_filename = 'dockersecret'
docker_secret = open(dockersecret_filename, 'r')

while True:
    line1 = docker_secret.readline()
    line2 = docker_secret.readline()
    line3 = docker_secret.readline()
    print 'line: ', line1
    print 'line2: ', line2
    print 'line3: ', line3
    if line1 == "" or line2 == "":
        print 'found a empty line: quiting'
        break
docker_secret.close()



# TODO: Check for configuration file exist and
# parse
def validate_config_file(config_file):
    with open(config_file, 'rt') as file_handle:
        xml_handle = ElementTree.parse(file_handle)

    for node in xml_handle.findall('.//organization'):
        bic8 = node.attrib.get('bic8')
        print bic8

data = dict()
data["Aorg3"]= []
data["Aorg3"].append(1)
data["Aorg3"].append(2)
data["Borg2"]=1
data["Aorg1"]=2
print 'sorted: ', sorted(data)

print 'b-reseting: ', data
init = ['1']
data["Aorg3"] = init
print 'a-reseting: ', data


list1 = list()
list1.append("A")
list1.append("B")
print "printing list", list1

set1 = set()
set1.add('c')
set1.add('a')
set1.add('a')
set1.add('a')
set1.add('a')
set1.add('a')
set1.update(list1)
print "printing set: ", set1

for item in set1:
    print 'set item - ', item

# file = open('tmp.json', 'r')
json_data = dict()
json_data = json.load(open('tmp.json', 'rw'))
print 'id ==> ', json_data['data']['id-type']
json_data['data'].update({'hello1': 'world'})
json_data['data'].update({'hello2': 'world'})
json_data['data']['arr'].append(list1[0])
json_data['data']['hello1'] = 'world1'
print json.dumps(json_data)



template = dict()
template = { 'name': "rahul1234"}
tmp_data = dict()
tmp_data['data']= json_data['data']
file_write = open('mod.json', 'w')
json.dump(template, file_write)
file_write.close()


args = argparse.ArgumentParser(description="Organization Crypto Management")
args.add_argument("--command",
                  choices=["generateCSRInMSP",
                           "collateCSRFromMSPForCA",
                           "pullPEMFromCA",
                           "distributePEMToMSP"],
                  help="sub commands supported by organization crypto-management",
                  action="store",
                  required="True",
                  dest="command")

args.add_argument("--config-file",
                  help="absolute path for the organization crypto management configuration file",
                  required="True",
                  action="store",
                  dest="config_file")

args.add_argument("--input-dirpath",
                  help="absolute path for input directory for command",
                  required="True",
                  action="store",
                  dest="input_dirpath")

args.add_argument("--output-dirpath",
                  help="absolute path for output directory for the command",
                  required="True",
                  action="store",
                  dest="output_dirpath")

args.add_argument("--bic8",
                  help="bic8 information of the organization, defaults to all bic8 in the configuration file",
                  default="all",
                  action="store",
                  dest="bic8")

args.add_argument("--force-update",
                  help="bic8 information of the organization, defaults to all bic8 in the configuration file",
                  action="store_true",
                  dest="force_update")

parsedArgs = args.parse_args()

print parsedArgs

validate_config_file(parsedArgs.config_file)

