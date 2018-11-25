#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
from tkinter import *
from kafka import KafkaProducer


master = Tk()
master.title("Know Your Credit Score")
Label(master, text="Credit Scoring Application",font='Helvetica 18 bold').grid(row=0,column=10)
Label(master, text="Salutation").grid(row=1)
Label(master, text="First Name").grid(row=2)
Label(master, text="Middle Name").grid(row=3)
Label(master, text="Last Name").grid(row=4)
Label(master, text="Name Suffix").grid(row=5)
Label(master, text="Address Line1").grid(row=6)
Label(master, text="Address Line2").grid(row=7)
Label(master, text="City").grid(row=8)
Label(master, text="State").grid(row=9)
Label(master, text="Zip").grid(row=10)
Label(master, text="SSN-Defaulted to the one available in Dataset").grid(row=11)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)
e7 = Entry(master)
e8 = Entry(master)
e9 = Entry(master)
e10 = Entry(master)
e11 = Entry(master)
e11.insert(END, '123-45-6789')

e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
e3.grid(row=3, column=1)
e4.grid(row=4, column=1)
e5.grid(row=5, column=1)
e6.grid(row=6, column=1)
e7.grid(row=7, column=1)
e8.grid(row=8, column=1)
e9.grid(row=9, column=1)
e10.grid(row=10, column=1)
e11.grid(row=11, column=1)


def kafka_name_publish():
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('ascii'))
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    payload_dict = {"nmPrefix": e1.get(),"fname": e2.get(), "mname": e3.get(), "lname": e4.get(), "nmSuffix": e5.get(),"addr1": e6.get(),"addr2": e7.get(),"city": e8.get(),"state": e9.get(),"zip": e10.get(),"ssn": e11.get()}
    payload_json=json.dumps(payload_dict)
    payload_byte=bytes(payload_json,'ascii')
    producer.send('nameParsing', payload_byte)
    producer.flush()


Button(master, text='Check your Score', command=kafka_name_publish).grid(row=13, column=5, sticky=W, pady=4)

mainloop( )

