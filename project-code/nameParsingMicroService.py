#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import json
import os
import re
from kafka import KafkaConsumer, KafkaProducer
class NameParsing:
    def __init__(self):
        self.name_dict = {}
    def name_parse(self,ssn,nmPrefix,fname,mname,lname,nmSuffix):
        nmPrefix=re.sub('[^A-Z.a-z]+', '', nmPrefix)
        fname=re.sub('[^A-Za-z]+', '', fname)
        mname=re.sub('[^A-Za-z]+', '', mname)
        lname=re.sub('[^A-Za-z]+', '', lname)
        nmSuffix=re.sub('[^A-Z.a-z]+', '', nmSuffix)
        parsedName=nmPrefix + " " + fname + " " + mname + " " + lname + " " + nmSuffix
        return parsedName
    def checkDb(self,key,fileName,index):
        with open(fileName,'r') as csvFile:
                csvReader=csv.reader(csvFile, delimiter=',')
                for row in csvReader:
                    if key == row[index]: # ssn is the first field
                        print ("Customer Record Exists")
                        lineNum = csvReader.line_num
                        print (lineNum)
                        return True
    def add_name(self,ssn,parsedName,custCsvName):
        with open (custCsvName,'a') as custCsvFile:
            csvWriter = csv.writer(custCsvFile, lineterminator='\n')
            row=ssn,parsedName
            csvWriter.writerow(row)

    print("Write to file successful!")



def parseMessage(newName):
    from kafka import KafkaConsumer
    consumer = KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))
    consumer.subscribe(['nameParsing'])
    for message in consumer:
        piiDict=message[6]
        #print(piiDict)
        nmPrefix=piiDict['nmPrefix']
        fname=piiDict['fname']
        lname=piiDict['lname']
        mname=piiDict['mname']
        nmSuffix=piiDict['nmSuffix']
        addr1=piiDict['addr1']
        addr2=piiDict['addr2']
        city=piiDict['city']
        state=piiDict['state']
        pin=piiDict['zip']
        ssn=piiDict['ssn']
        ssn=re.sub('[^0-9]+','',ssn)
        parsedName=newName.name_parse(ssn,nmPrefix,fname,mname,lname,nmSuffix)
        def add_nm(newName):
            custCsvName='custDirectory.csv'
            if not os.path.exists(custCsvName):
                with open (custCsvName,'w') as custCsvFile:
                    csvWriter = csv.writer(custCsvFile, lineterminator='\n')
                    csvWriter.writerow(("SSN","PARSED NAME"))
            dbHit=newName.checkDb(ssn,custCsvName,0)
            print(dbHit)
            if(dbHit):
                print("Customer Exists")
            else:
                parsedName=newName.name_parse(ssn,nmPrefix,fname,mname,lname,nmSuffix)
                newName.add_name(ssn,parsedName,custCsvName)
        add_nm(newName)
        def kafka_publish(newName):
            from kafka import KafkaProducer
            producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('ascii'))
            producer = KafkaProducer(bootstrap_servers='localhost:9092')
            payload_dict = {"ssn": ssn,"parsedName": parsedName, "addr1": addr1, "addr2": addr2, "city": city,"state": state,"zip": pin}
            payload_json=json.dumps(payload_dict)
            payload_byte=bytes(payload_json,'ascii')
            producer.send('addressParsing', payload_byte)
            producer.flush()
        kafka_publish(newName)
    
        
#main
newName = NameParsing()
parseMessage(newName)

