import time
import mysql.connector
import requests
import urllib.request
import signal

import json
import configparser as cfg
import numpy as np

import telegram.ext
from telegram import ReplyKeyboardMarkup

from datetime import timezone
from datetime import datetime
import random

#import pandas as pd
#import os
#from bokeh.io import output_notebook
#import telegram
#import urllib.request#, json



class databasechatbot(object):
    def __init__(self):

        self.offset = 1
        self.urlold = "start"
        self.i = 0
        self.update_id = 1
        self.urlupdategrenze = 50
        self.execution_timeout = 50
        
        #database
        self.databaseuser='server_bergnungpython'
        self.databasepwd='RHlSEVvFAr6kVcFr'
        self.databasehost='162.55.0.136'
        self.database='server_Beregnung'
        
        #telegram
        self.tokens = "6216581879:AAGZAKidYqS_OhtxYMlg61D2RgB6daXjq4c"
        self.base = "https://api.telegram.org/bot{}/".format(self.tokens)
        
        #self.cnx = mysql.connector.connect(user='server_bergnungpython', password='RHlSEVvFAr6kVcFr',host='server.bplaced.net',database='server_Beregnung')
        print("init")
        
    def databaseconnectio(self):
        self.cnx = mysql.connector.connect(user=self.databaseuser, password=self.databasepwd,host=self.databasehost,database=self.database)
        #print("init")
        
        runcon = False
        
        while runcon == False:
    

            try:

                self.cnx = mysql.connector.connect(user=self.databaseuser, password=self.databasepwd,host=self.databasehost,database=self.database)
                if (self.cnx.is_connected()):
                    print("Connected")
                    runcon = True
        
                self.mycursor = self.cnx.cursor()

            except Exception as e:

                dt = datetime.datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                utc_timestamp_now = utc_time.timestamp()

                dt_string = str(utc_timestamp_now)
                dt_string = str(utc_time.strftime("%d/%m/%Y %H:%M:%S"))
                with open("log.txt","a") as error:
                    error.write(""+dt_string+" dyn "+str(e)+"\n")
        
                print("connect failed")
                print(e)
                runcon = False

        return self.mycursor

    def get_updates(self):
        
        '''
        try:

            url = self.base + "getUpdates?timeout=1"
            url = url + "&offset={}".format(self.update_id + self.offset)
            r = requests.get(url)
            #print(url)
            
        except:
            print("no update")
        #print(self.urlold)
        #idnow=url.lstrip("https://api.telegram.org/bot1061616188:AAFJIaCjjQ3N-iGegrrexclCNtg4BJblhwA/getUpdates?timeout=2&offset")
        #idnow =int(idnow)
        #print()
        #if url==self.urlold:
        #    self.i+=1
        #    print(self.i)
        #    self.offset = 1
            
        #if self.i==self.urlupdategrenze:
         #   self.offset = 2
         #   self.i=0
            
        self.urlold = url  

        '''
        runcon = False
        
        while runcon == False:

            print("second")

            try:

                print("third")
                url = self.base + "getUpdates?timeout=1"
                print(5)
                url = url + "&offset={}".format(self.update_id + self.offset)
                print(6)
                #time.sleep(3)
                r = requests.get(url,timeout=4)
                print(r)
                print(7)
                print("Connected_telegram")
                runcon = True

            except Exception as e:
        
                print("connect failed")
                print(e)
                runcon = False                 

        return json.loads(r.content)
    
    def send_keyboard(self):
        self.mycursor = self.databaseconnectio()
        chat_ids=[]
        #mycursor = self.cnx.cursor()
        self.mycursor.execute("SELECT telgrammchatid_1,telgrammchatid_2,telgrammchatid_3 FROM benutzerdaten_demo")  
        mods = self.mycursor.fetchall()

        for x in mods:

            chat_ids.append(x[0])
            chat_ids.append(x[1])
            chat_ids.append(x[2])
        chat_ids = list(dict.fromkeys(chat_ids))
        chat_ids.remove('')
        #print(chat_ids)
        
        for chat_id in chat_ids:
            menu_keyboard = [['/aktueller_Standort']] #angepasst
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True, remove_keyboard=True)
            self.bot.send_message(chat_id=chat_id,text="restart bot", reply_markup=menu_markup)
        self.mycursor.close()

    def send_message(self, msg, chat_id, moduls, betriebsnummerarray):
        
        #moduls, betriebsnummerarray = objName.module(str(chat_id))#+++++++
        
        if msg == "/aktueller_Standort" or msg == "/start": #angepasst
            
            menu_keyboard = np.array(moduls).reshape(-1, 1)
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True, remove_keyboard=False)
            #print(chat_id)
            self.bot.send_message(chat_id=chat_id,text="wähle eine Beregnung aus", reply_markup=menu_markup)
        
        if msg in moduls:

            latarray=[]
            lngarray=[]
            statusarray=[]
            
            msg= msg.replace("/", "") #angepasst
            #mycursor = self.cnx.cursor()
            print("betriebsnumarray")
            print(betriebsnummerarray[0])
            self.mycursor = self.databaseconnectio()
            self.mycursor.execute("SELECT * FROM all_in_one_demo WHERE Modulname = '"+msg+"'AND Betriebsnummer = '"+betriebsnummerarray[0]+"' AND Lat != 'X' ORDER BY Zeit DESC LIMIT 1")
            status = self.mycursor.fetchall()
            self.mycursor.close()
            for z in status:

                latarray.append(z[7])
                lngarray.append(z[8])
                statusarray.append(z[11])
            
            #print(chat_id,latarray[0], lngarray[0])
            #latn = round(float(latarray[0]),1)
            #lngn = round(float(lngarray[0]),1)
             
            
            #print(latn, lngn)
            
            
            if statusarray[0]=="0":
                msg = msg+' ❌'
                #print("hdf")
            if statusarray[0]=="1":
                msg = msg+' ✅'
                
            menu_keyboard = [['/aktueller_Standort']] #angepasst
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True, remove_keyboard=False)
            print(latarray[0])
            print(lngarray[0])
            self.bot.send_location(chat_id,latarray[0], lngarray[0])
            self.bot.send_message(chat_id=chat_id,text=msg, reply_markup=menu_markup) 
            
    #def send_button(self, msg, chat_id):
       # url = self.base + "reply_markup?chat_id={}&text={}".format(chat_id, msg)
       # print("hi")
       # if msg is not None:
           # requests.get(url)
            
    def module(self,chat_id):
        
        self.mycursor = self.databaseconnectio()
        betriebsnumarray=[]
        moarray=[]
        #print("cnx:")
        #print(self.cnx)
        
        #t= self.cnx
        #mycursor = t.cursor()
        
        self.mycursor.execute("SELECT * FROM benutzerdaten_demo WHERE telgrammchatid_1 = '"+chat_id+"' OR telgrammchatid_2 = '"+chat_id+"' OR telgrammchatid_3 = '"+chat_id+"'")  
        mods = self.mycursor.fetchall()

        self.mycursor.close()

        for x in mods:

            betriebsnumarray.append(x[9])

        betriebsnumarray = list(dict.fromkeys(betriebsnumarray))
        
        self.mycursor = self.databaseconnectio()
        self.mycursor.execute("SELECT * FROM all_in_one_demo WHERE Betriebsnummer = '"+betriebsnumarray[0]+"'")  
        mo = self.mycursor.fetchall()
        self.mycursor.close()
        
        for y in mo:

            moarray.append("/"+y[3])
            #print(y[3])
        moarray = list(dict.fromkeys(moarray))
        #print(moarray)

        return moarray, betriebsnumarray
    
    def handler(self,signum,frame):
        print("time is over!")
        raise Exception("end of time")
                        
    def main(self):
    
    
        try:
            #self.internet_on()
            self.bot = telegram.Bot(token=self.tokens)
            #self.mycursor = self.databaseconnectio()
            self.send_keyboard()
            
        except:
            print("wrong start")

        signal.signal(signal.SIGALRM, self.handler)
            
        while True:
            
            try:
                signal.alarm(self.execution_timeout)
                self.bot = telegram.Bot(token=self.tokens)
                #self.bot.close()
                updates=[]
                item=[]
                moduls=[]
                betriebsnummerarray=[]
                message = None

                print("random")
                print(random.randint(0,9))
                print("first")
                updates = self.get_updates()
                print(updates)
                updates = updates["result"]
                #print(updates)
                if updates:
                    for item in updates:

                        self.update_id = item["update_id"]
                        message = str(item["message"]["text"])
                        from_ = item["message"]["chat"]["id"]
                        
                        sec_post = item["message"]["date"]
                        sec_now = int(round(time.time()))
                        
                        time_dif = sec_now-int(sec_post)
                        print("-----")
                        print(time_dif)
                        print("-----")
                        
                        if time_dif<100:
                            
                            #self.mycursor = self.databaseconnectio()
                            moduls, betriebsnummerarray = self.module(str(from_))
                            #print(moduls)
                            #print("---------")
                            self.send_message(message, from_, moduls, betriebsnummerarray)
                            #self.mycursor.close()        
            #except:
               # print("retry")
                #time.sleep(60)
            
            except Exception as e:
            
                now = datetime.now()
 
                print("now =", now)
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                with open("log.txt","a") as error:
                    error.write(""+dt_string+" dyn "+str(e)+"\n")
                    
                print(e)
                print("retry")        
            

if __name__ == '__main__':
    objName = databasechatbot()
    objName.main()
