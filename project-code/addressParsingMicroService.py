#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import json
import os
import re
from kafka import KafkaConsumer, KafkaProducer
class AddressParsing:
    def __init__(self):
        self.addr_dict = {}
    def addr_parse(self,ssn,addr1,addr2,city,state,pin):
        addr1=re.sub('[^A-Z.a-z0-9\s]+', '', addr1)
        addr1=re.sub('LANE'.upper(), 'LN', addr1.upper())
        addr1=re.sub('CIRCLE'.upper(), 'CIR', addr1.upper())
        addr1=re.sub('STREET'.upper(), 'ST', addr1.upper())
        addr1=re.sub('DRIVE'.upper(), 'DR', addr1.upper())
        addr2=re.sub('[^A-Za-z0-9\s]+', '', addr2.upper())
        addr2=re.sub('APARTMENT'.upper(), 'APT', addr2.upper())
        city=re.sub('[^A-Za-z]+', '', city.upper())
        state=re.sub('[^A-Z]+', '', state.upper())
        pin=re.sub('[^0-9]+', '', pin)
        parsedAddr=addr1 + "," + addr2 + "  " + city + " " + state + " " + pin
        return parsedAddr
    def checkDb(self,key,fileName,index):
        with open(fileName,'r') as csvFile:
                csvReader=csv.reader(csvFile, delimiter=',')
                for row in csvReader:
                    if key == row[index]: # ssn is the first field
                        print ("Customer Record Exists")
                        lineNum = csvReader.line_num
                        print (lineNum)
                        return True
    def add_addr(self,ssn,parsedAddr,custCsvName):
        with open (custCsvName,'a') as custCsvFile:
            csvWriter = csv.writer(custCsvFile, lineterminator='\n')
            row=ssn,parsedAddr
            csvWriter.writerow(row)

    print("Write to file successful!")



def parseMessage(newAddr):
    from kafka import KafkaConsumer
    consumer = KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))
    consumer.subscribe(['addressParsing'])
    for message in consumer:
        piiDict=message[6]
        #print(piiDict)
        parsedName=piiDict['parsedName']
        addr1=piiDict['addr1']
        addr2=piiDict['addr2']
        city=piiDict['city']
        state=piiDict['state']
        pin=piiDict['zip']
        ssn=piiDict['ssn']
        ssn=re.sub('[^0-9]+','',ssn)
        #print (nmPrefix,fname,mname,lname,nmSuffix,ssn)
        parsedAddr=newAddr.addr_parse(ssn,addr1,addr2,city,state,pin)
        def add_addr(newAddr):
            addrCsvName='addrDirectory.csv'
            if not os.path.exists(addrCsvName):
                with open (addrCsvName,'w') as addrCsvFile:
                    csvWriter = csv.writer(addrCsvFile, lineterminator='\n')
                    csvWriter.writerow(("SSN","PARSED ADDRESS"))
            dbHit=newAddr.checkDb(ssn,addrCsvName,0)
            print(dbHit)
            if(dbHit):
                print("Address Record Exists")
            else:
                parsedAddr=newAddr.addr_parse(ssn,addr1,addr2,city,state,pin)
                print(parsedAddr)
                newAddr.add_addr(ssn,parsedAddr,addrCsvName)
        add_addr(newAddr)
        def kafka_publish(newAddr):
            from kafka import KafkaProducer
            producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('ascii'))
            producer = KafkaProducer(bootstrap_servers='localhost:9092')
            payload_dict = {"ssn": ssn,"parsedName": parsedName, "parsedAddr": parsedAddr}
            payload_json=json.dumps(payload_dict)
            payload_byte=bytes(payload_json,'ascii')
            producer.send('score', payload_byte)
            producer.flush()
        kafka_publish(newAddr)

    
        
#main
newAddr = AddressParsing()
parseMessage(newAddr)

