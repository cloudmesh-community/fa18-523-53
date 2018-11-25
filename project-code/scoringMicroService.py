#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import json
import os
import re
import tk_tools
import datetime
import time
from tkinter import *
from kafka import KafkaConsumer, KafkaProducer
class Scoring:
    def __init__(self):
        self.score_dict = {}
    def checkDb(self,key,fileName,index):
        with open(fileName,'r') as csvFile:
                csvReader=csv.reader(csvFile, delimiter=',')
                for row in csvReader:
                    if key == row[index]: # ssn is the first field
                        print ("Customer Record Exists")
                        lineNum = csvReader.line_num
                        print (lineNum)
                        return True
    def get_attr(self,key,creditCsvName,index):
        with open (creditCsvName,'r') as custCsvFile:
            csvReader = csv.reader(custCsvFile, delimiter=',')
            for row in csvReader:
                    if key == row[index]: # ssn is the first field
                        attr_dict = {"active_since" : row[1] , "inquiries" : row[2] , "creditLimit" : row[3] , "totBalance" : row[4] , "PRFlag" : row[5] , "missedPayments" : row[6] }                       
                        return attr_dict
    def calc_score(self,attr_dict):
        max_score=850
        credit_dict=attr_dict
        inquiries_cut=int(attr_dict['inquiries'])*10
        new_score=max_score-int(inquiries_cut)
        if attr_dict['PRFlag'] == "Y":
            new_score=new_score-200
        missed_pymnts_cut=int(attr_dict['missedPayments'])*100
        new_score=new_score-100
        util_percentage=round((int(attr_dict['totBalance'])*100)/int(attr_dict['creditLimit']),2)
        print (util_percentage)
        if (util_percentage>10 and util_percentage <20):
            new_score=new_score-20
        elif (util_percentage>20 and util_percentage <30):
            new_score=new_score-30
        elif (util_percentage>30 and util_percentage <40):
            new_score=new_score-40
        elif (util_percentage>40 and util_percentage <50):
            new_score=new_score-50
        elif (util_percentage<10):
            new_score=new_score-0
        else:
            new_score=new_score-100
        credit_dict["score"]=new_score
        return credit_dict
    def output_UI(self,credit_dict):
            if credit_dict['PRFlag']=="Y":
                derogatory="Found Derogatory Marks on the record"
            else:
                derogatory="No Derogatory Marks on the Record"
            util_percentage=round((int(credit_dict['totBalance'])*100)/int(credit_dict['creditLimit']))
            currentDateTime=datetime.datetime.now().strftime("%Y-%m-%d")
            currentDateTime=time.strptime(currentDateTime, "%Y-%m-%d")
            creditSincedate = time.strptime(credit_dict['active_since'], "%Y-%m-%d")
            yearsActive=currentDateTime.tm_year - creditSincedate.tm_year
            master = Tk()
            master.title("Credit Score Dashboard")
            master.configure(background='white')
            #Score Guage
            score_gauge = tk_tools.Gauge(master, height=250, width=500,
                            max_value=850,
                            min_value=350,
                            label='Score',
                            divisions=10, 
                            red_low=30, yellow_low=70,yellow=110,red=120, bg='white')
            score_gauge.grid(row=1, column=2, sticky='news')
            score_gauge.set_value(credit_dict['score'])
            Label(master, text="Your Credit Score is " + str(credit_dict['score']),font='Helvetica 18 bold').grid(row=2,column=2)
            Label(master, text="Active Since " + str(credit_dict['active_since']),font='Helvetica 18 bold').grid(row=3,column=2)
            Label(master, text="Total Inquiries are " + str(credit_dict['inquiries']),font='Helvetica 18 bold').grid(row=4,column=2)
            Label(master, text="Utilization percentage is " + str(util_percentage) + "%",font='Helvetica 18 bold').grid(row=5,column=2)
            Label(master, text=derogatory,font='Helvetica 18 bold').grid(row=6,column=2)
            Label(master, text="Missed Payments as of today are " + str(credit_dict['missedPayments']),font='Helvetica 18 bold').grid(row=7,column=2)
            #Inquiry Guage
            inquiry_gauge = tk_tools.Gauge(master, height=250, width=300,
                            max_value=20,
                            min_value=0,
                            label='Inquiries',
                            divisions=10, 
                            red_low=-1, yellow_low=-1,yellow=50,red=90, bg='white')
            inquiry_gauge.grid(row=8, column=1, sticky='news')
            inquiry_gauge.set_value(credit_dict['inquiries'])
            #Utilization Guage
            util_gauge = tk_tools.Gauge(master, height=250, width=500,
                            max_value=100,
                            min_value=0,
                            label='Utilization',
                            unit='%',
                            divisions=10, 
                            red_low=-1, yellow_low=-1,yellow=30,red=60, bg='white')
            util_gauge.grid(row=8, column=2, sticky='news')
            util_gauge.set_value(util_percentage)
            #Missed Payments Guage
            payments_gauge = tk_tools.Gauge(master, height=250, width=300,
                            max_value=100,
                            min_value=0,
                            label='Missed Payments',
                            divisions=10, 
                            red_low=-1, yellow_low=-1,yellow=10,red=20, bg='white')
            payments_gauge.grid(row=8, column=3, sticky='news')
            payments_gauge.set_value(credit_dict['missedPayments'])
            #Active Since Guage
            active_since_gauge = tk_tools.Gauge(master, height=250, width=300,
                            max_value=80,
                            min_value=0,
                            label='Years Active',
                            unit="Years",
                            divisions=16, 
                            red_low=4, yellow_low=8,yellow=110,red=120, bg='white')
            active_since_gauge.grid(row=8, column=4, sticky='news')
            active_since_gauge.set_value(yearsActive)
            mainloop( )
    print("Write to file successful!")



def parseMessage(score):
    from kafka import KafkaConsumer
    consumer = KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))
    consumer.subscribe(['score'])
    for message in consumer:
        piiDict=message[6]
        #print(piiDict)
        parsedName=piiDict['parsedName']
        parsedAddr=piiDict['parsedAddr']
        ssn=piiDict['ssn']
        ssn=re.sub('[^0-9]+','',ssn)
        def get_score(score):
            creditCsvName='creditDatabase.csv'
            dbHit=score.checkDb(ssn,creditCsvName,0)
            print(dbHit)
            if(dbHit):
                print("Credit Record Exists")
                attr_dict=score.get_attr(ssn,creditCsvName,0)
                print (attr_dict) 
                credit_dict=score.calc_score(attr_dict)
                print(credit_dict)
                score.output_UI(credit_dict)
            else:
                master = Tk()
                master.title("Credit Score Dashboard")
                master.configure(background='white')
                Label(master, text="Credit Record Doesnot Exist",font='Helvetica 18 bold').grid(row=2,column=2)
                mainloop( )
        get_score(score)
        
    
        
#main
score = Scoring()
parseMessage(score)

