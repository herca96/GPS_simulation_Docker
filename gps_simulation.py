import time
import mysql.connector
import signal
from datetime import timezone
from datetime import datetime
import datetime
import os
import logging

# Logging configuration
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s [in %(filename)s:%(lineno)d, %(funcName)s]',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.info("Initialization complete")

# import pandas as pd

databaseuser = os.getenv("DATABASE_USER")
databasepwd = os.getenv("DATABASE_PASSWORD")
databasehost = os.getenv("DATABASE_HOST")
database = os.getenv("DATABASE_NAME")
execution_timeout = 50

Latarray = [52.38279, 52.382745, 52.382603, 52.382553, 52.382526, 52.382485]
Lonarray = [10.330706, 10.330296, 10.3297, 10.329196, 10.328746, 10.328196]

Device = "FHeidmann1"
Modulname = "Huedig_2"
Betriebsname = "Heidmann"
Betriebsnummer = 2
Rohdaten = "X"
Temperatur = "X"
Spannung = "X"
Status = 1

logging.info("start gps simulation")

while True:
    for Lat, Lng in zip(Latarray, Lonarray):
        print("ok")
        #logging.info("Starting new iteration with Lat: %s, Lng: %s", Lat, Lng)

        try:
            # signal.alarm(execution_timeout)

            cnx = mysql.connector.connect(user=databaseuser, password=databasepwd, host=databasehost, database=database)

            if cnx.is_connected():
                print("Connected")
                #logging.info("Connected to the database")
                runcon = True

            mycursor = cnx.cursor()
            print("connected1")
            #logging.info("Cursor created")

            mycursor.execute("INSERT INTO all_in_one (Device, Modulname, Betriebsname, Betriebsnummer, Rohdaten, Lat, Lng, Temperatur, Spannung, Status) VALUES ('" + str(Device) + "', '" + str(Modulname) + "','" + str(Betriebsname) + "','" + str(Betriebsnummer) + "','" + str(Rohdaten) + "','" + str(Lat) + "','" + str(Lng) + "','" + str(Temperatur) + "','" + str(Spannung) + "','" + str(Status) + "')")
            cnx.commit()
    

        except Exception as e:

            print("connect failed")
            print(e)
            logging.error("Connection failed: %s", e)
            runcon = False

        time.sleep(240)  # 4 min

    logging.info("Iteration finsihsed")

    time.sleep(1200)  # 20 min