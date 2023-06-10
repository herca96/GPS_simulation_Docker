import time
import mysql.connector
import requests
import urllib.request
import signal

import json
import configparser as cfg
import numpy as np

from datetime import timezone
from datetime import datetime
import datetime

import telegram.ext
from telegram import ReplyKeyboardMarkup
#import pandas as pd

databaseuser='server_bergnungpython'
databasepwd='RHlSEVvFAr6kVcFr'
databasehost="162.55.0.136"#'server.bplaced.net'
database='server_Beregnung'
execution_timeout = 50

#pathprotopath = "./GPS_Data_to_analyse/errreq.pb"

#pathprotopath = "./GPS_Data_to_analyse/errreq.pb"

Latarray=[52.38279,52.382745,52.382603,52.382553,52.382526,52.382485]
Lonarray=[10.330706,10.330296,10.3297,10.329196,10.328746,10.328196]

def handler(signum,frame):
    print("time is over!")
    #raise Exception("end of time")

signal.signal(signal.SIGALRM, handler)

while True:

    for Lat,Lng in zip(Latarray,Lonarray):

        Device = 1111
        Modulname = "DeierlingX"
        Betriebsname = "test46"
        Betriebsnummer = 46
        Rohdaten = "X"
        #Lat = 52.38
        #Lng = 10.38
        Temperatur = "X"
        Spannung = "X"
        Status = 1

        print("ok")

        try:

            signal.alarm(execution_timeout)

            cnx = mysql.connector.connect(user=databaseuser, password=databasepwd,host=databasehost,database=database)


            if (cnx.is_connected()):
                print("Connected")
                runcon = True

            mycursor = cnx.cursor()
            print("connected1")


            mycursor.execute("INSERT INTO all_in_one_demo (Device, Modulname, Betriebsname,Betriebsnummer,Rohdaten,Lat,Lng,Temperatur,Spannung,Status) VALUES ('"+str(Device)+"', '"+str(Modulname)+"','"+str(Betriebsname)+"','"+str(Betriebsnummer)+"','"+str(Rohdaten)+"','"+str(Lat)+"','"+str(Lng)+"','"+str(Temperatur)+"','"+str(Spannung)+"','"+str(Status)+"')")#AND Update all_in_one set status = 1 where id = '"+str(idnr_2)+"'AND Update all_in_one set status = 1 where id = '"+str(idnr_1)+"'")  #status ändern 3+4  eigentlich
            cnx.commit()
                #mycursor.execute("INSERT INTO benutzerdaten_test (Vorname,Nachname,email) VALUES ('"+str(Vorname)+"')")#AND Update all_in_one set status = 1 where id = '"+str(idnr_2)+"'AND Update all_in_one set status = 1 where id = '"+str(idnr_1)+"'")  #status ändern 3+4  eigentlich
                #cnx.commit()

        except Exception as e:

            dt = datetime.datetime.now(timezone.utc)
            utc_time = dt.replace(tzinfo=timezone.utc)
            utc_timestamp_now = utc_time.timestamp()

            dt_string = str(utc_timestamp_now)
            dt_string = str(utc_time.strftime("%d/%m/%Y %H:%M:%S"))
            #with open("log.txt","a") as error:
            #    error.write(""+dt_string+" dyn"+str(e)+"\n")

            print("connect failed")
            print(e)
            runcon = False
            
        time.sleep(20)

    time.sleep(240)
    

