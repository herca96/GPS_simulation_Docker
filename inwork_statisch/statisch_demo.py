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
        self.databasehost="162.55.0.136"#'server.bplaced.net'
        self.database='server_Beregnung'
        
        #telegram
        self.tokens = "6216581879:AAGZAKidYqS_OhtxYMlg61D2RgB6daXjq4c"
        self.base = "https://api.telegram.org/bot{}/".format(self.tokens)
        
        #self.cnx = mysql.connector.connect(user='server_bergnungpython', password='RHlSEVvFAr6kVcFr',host='server.bplaced.net',database='server_Beregnung')
        print("init")
        
    def databaseconnectio(self):

           # self.cnx = mysql.connector.connect(user=self.databaseuser, password=self.databasepwd,host=self.databasehost,database=self.database)
            #print("init")
            
        runcon = False
        
        while runcon == False:

            try:

                self.cnx = mysql.connector.connect(user=self.databaseuser, password=self.databasepwd,host=self.databasehost,database=self.database)
                if (self.cnx.is_connected()):
                    print("Connected")
                    runcon = True
        
                self.mycursor = self.cnx.cursor()
                print("connected1")

            except Exception as e:

                time.sleep(1)

                dt = datetime.datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                utc_timestamp_now = utc_time.timestamp()

                dt_string = str(utc_timestamp_now)
                dt_string = str(utc_time.strftime("%d/%m/%Y %H:%M:%S"))
                with open("log.txt","a") as error:
                    error.write(""+dt_string+" stat_"+str(e)+"\n")
        
                print("connect failed")
                print(e)
                runcon = False

        return self.mycursor

    
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
            #menu_keyboard = [['/aktueller_Standort']] #angepasst
            #menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False, resize_keyboard=True, remove_keyboard=True)
            self.bot.send_message(chat_id=chat_id,text="restartauswertbot")

        self.mycursor.close()

    def send_message(self, msg, lat_0, lng_0, modulname, betriebsnummer):
        
        #moduls, betriebsnummerarray = objName.module(str(chat_id))#+++++++
        self.mycursor = self.databaseconnectio()

         
        chat_ids=[]
        #mycursor = self.cnx.cursor()
        self.mycursor.execute("SELECT telgrammchatid_1,telgrammchatid_2,telgrammchatid_3 FROM benutzerdaten_demo WHERE betriebsnummer = "+betriebsnummer+"")  
        mods = self.mycursor.fetchall()

        self.mycursor.close()

        for x in mods:

            chat_ids.append(x[0])
            chat_ids.append(x[1])
            chat_ids.append(x[2])
        chat_ids = list(dict.fromkeys(chat_ids))
        chat_ids.remove('')
        #print(chat_ids)
        
        
        for i in chat_ids:
        
            if msg=="aus":
                send = modulname+' ❌'
                #print("hdf")
            if msg=="an":
                send = modulname+' ✅'

            self.bot.send_location(i,lat_0, lng_0)
            self.bot.send_message(chat_id=i,text=send) 
            
    #def send_button(self, msg, chat_id):
       # url = self.base + "reply_markup?chat_id={}&text={}".format(chat_id, msg)
       # print("hi")
       # if msg is not None:
           # requests.get(url)
            
    def module(self):
        
        self.mycursor = self.databaseconnectio()

        betriebsnumarray=[]
        moarray=[]

        timeout = 3 #context.execution_options.get('timeout', None)
        #if timeout:
        #c = cursor.connection.cursor()
        #self.mycursor.execute('SET SESSION MAX_EXECUTION_TIME= 1000')
        #self.mycursor.close()
        #return execute(cursor, statement, parameters, context)

        
        #self.new_method()
        #print("true")
        #self.mycursor.execute('SET SESSION MAX_EXECUTION_TIME=%d;' % int(timeout * 1000))
        #self.mycursor.execute("SELECT /*+ MAX_EXECUTION_TIME(10) */ status, Device FROM all_in_one") 

        self.mycursor.execute("SELECT Device FROM all_in_one_demo")

        #pr1.start()
        #self.mycursor.execute("SELECT Device FROM all_in_one")   
        mods = self.mycursor.fetchall()
        
        for i in mods:
            moarray.append(i[0])
        
        modulliste = list(dict.fromkeys(moarray)) # liste mit allen Modulen

        self.mycursor.close()
        
        #print(modulliste)
        return modulliste

    #def new_method(self):
        
        #self.mycursor.execute("SELECT Device FROM all_in_one")
        
        
    def lastone(self,modulliste):

        self.mycursor = self.databaseconnectio()
        
        
        alleletztendatenarray = []
        alleletztendaten = []
        
        for x in modulliste:
        
            idnr = []
            zeit = []
            device = []
            modulname = []
            betriebsname = []
            betriebsnr = []
            #rohdaten = []
            lat = []
            lng = []
            #temp = []
            #spannung = []
            status = []
            
            alleletztendaten = []

            #$tbwerte= "SELECT * FROM Sigfox_Rohdaten WHERE Betriebsname = '$betrieb'";
            #print("module")
            #print(x)
            #print('module')
            self.mycursor.execute("SELECT * FROM all_in_one_demo WHERE Device = '"+str(x)+"' AND Lat != 'X' ORDER BY Zeit DESC LIMIT 5")
            latestdata = self.mycursor.fetchall()
            
            
            
            for x in latestdata:
            
                idnr.append(x[0])
                zeit.append(x[1])
                device.append(x[2])
                modulname.append(x[3])
                betriebsname.append(x[4])
                betriebsnr.append(x[5])
                #rohdaten.append(x[6])
                lat.append(x[7])
                lng.append(x[8])
                #temp.append(x[9])
                #spannung.append(x[10])
                status.append(x[11])
                
                
            idnrnumarray = list(idnr)
            zeitnumarray = list(zeit)
            devicenumarray = list(device)
            modulnamenumarray = list(modulname)
            betriebsnamenumarray = list(betriebsname)
            betriebsnrnumarray = list(betriebsnr)
            latnumarray = list(lat)
            lngnumarray = list(lng)
            statusnumarray = list(status)
            
            
            #if idnrnumarray != "0" and  zeitnumarray != "0" and devicenumarray != "0" and latnumarray != "0":
            if idnrnumarray and zeitnumarray and devicenumarray and latnumarray:
            
            
                alleletztendaten = [idnrnumarray,zeitnumarray,devicenumarray,modulnamenumarray,betriebsnamenumarray,betriebsnrnumarray,latnumarray,lngnumarray,statusnumarray]


                alleletztendatenarray.append(alleletztendaten)
        
        #print("alleletzendaten")
        #print(alleletztendatenarray)
        #print("alleletzendaten")
        self.mycursor.close()
        
        return alleletztendatenarray
        
        
        
    def auswertung(self, alleletztendatenarray):
        
        betriebsnumarray=[]
        moarray=[]
        #print("cnx:")
        #print(self.cnx)
        
        #t= self.cnx
        #mycursor = t.cursor()
        
        #self.mycursor.execute("SELECT * FROM all_in_one Device")
        #mods = self.mycursor.fetchall()
        
        #modulliste = list(dict.fromkeys(mods)) # liste mit allen Modulen
        
        for x in alleletztendatenarray:
        
        #alleletztendaten = [idnrnumarray,zeitnumarray,devicenumarray,modulnamenumarray,betriebsnamenumarray,betriebsnrnumarray,latnumarray,lngnumarray,statusnumarray]
            
            try:

                idnr = x[0]
                zeit = x[1]
                device = x[2]
                modulname = x[3]
                betriebsname = x[4]
                betriebsnr = x[5]
                lat = x[6]
                lng = x[7]
                status = x[8]
                
                idnr_0 = idnr[0]
                #print(idnr_0)
                zeit_0 = zeit[0]
                device_0 = device[0]
                modulname_0 = modulname[0]
                betriebsname_0 = betriebsname[0]
                betriebsnr_0 = betriebsnr[0]
                lat_0 = lat[0]
                lng_0 = lng[0]
                status_0 = status[0]
                
                idnr_1 = idnr[1]
                zeit_1 = zeit[1]
                device_1 = device[1]
                modulname_1 = modulname[1]
                betriebsname_1 = betriebsname[1]
                betriebsnr_1 = betriebsnr[1]
                lat_1 = lat[1]
                lng_1 = lng[1]
                status_1 = status[1]
                
                status_2 = status[2]
                status_3 = status[3]
                #status_4 = status[4]
                idnr_2 = idnr[2]
                idnr_3 = idnr[3]
            

            
                dt = datetime.datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                utc_timestamp_now = utc_time.timestamp()
                
                #print(dt)
                
                
                
                
                utc_time_latest = zeit_0.replace(tzinfo=timezone.utc)
                utc_timestamp_latest = utc_time_latest.timestamp()
                
                #print("xxxx")
                #print(utc_timestamp_now+7200)
                #print(utc_timestamp_latest)
                #print("xxxxx")
                
                #print(zeit_0)
                
                time_dif = ((utc_timestamp_now+3600) - (utc_timestamp_latest))/60  #sommerzeit +7200 winterzeit +3600
                
                #print("difftime")
                #print(time_dif)
                #print("difftime")

                
                #print("-------------")
                #print(betriebsname_0)
                #print(modulname_0)
                #print(status_0)
                #print(status_1)
                #print(status_2)
                #print(status_3)
                #print(status_4)
                #print("-------------")
                
                
                    
                if time_dif > 15: #über 15 min
                

                
                    if int(status_0) != 0: #status auf 0 setzen, wenn noch nicht passiert
                        
                        #print(idnr_0)
                        self.mycursor = self.databaseconnectio()
                    
                        self.mycursor.execute("Update all_in_one_demo set status = 0 where id = '"+str(idnr_0)+"'")  #status ändern
                        self.cnx.commit()
                        #print("status geändert") 
                        
                        time.sleep(1)
                        self.mycursor.close()
                        

                    
                    if int(status_0) == 0 and int(status_1) == 1: #einmalig nachricht aus schicken 
                    
                    # 
                        #if int(status_1) == 1 and int(status_2) == 1 and int(status_3) == 1 and int(status_4) == 1:
                        
                        #print("AUS")
                        self.send_message("aus", lat_0, lng_0, modulname_0, betriebsnr_0)
                        self.mycursor = self.databaseconnectio()
                        #print(idnr_1)

                        self.mycursor.execute("Update all_in_one_demo set status = 0 where id = '"+str(idnr_1)+"'")  #status ändern
                        self.cnx.commit()
                        
                        
                        #setze 
                        
                        
                        
                        time.sleep(1)
                        self.mycursor.close()
                        
                    
            
                
                if int(status_0) == 1 and int(status_1) == 0 : #and int(status_2) == 1 and int(status_3) == 0  and int(status_4) == 0: #änderung zu an
                

                    
                    self.send_message("an", lat_0, lng_0, modulname_0, betriebsnr_0)
                    self.mycursor = self.databaseconnectio()
                    #self.mycursor.execute("Update all_in_one set status = 1 where id = '"+str(idnr_3)+"'AND Update all_in_one set status = 1 where id = '"+str(idnr_2)+"'AND Update all_in_one set status = 1 where id = '"+str(idnr_1)+"'")  #status ändern
                    self.mycursor.execute("Update all_in_one_demo set status = 1 where id IN ('"+str(idnr_2)+"','"+str(idnr_1)+"')")#AND Update all_in_one set status = 1 where id = '"+str(idnr_2)+"'AND Update all_in_one set status = 1 where id = '"+str(idnr_1)+"'")  #status ändern 3+4  eigentlich

                    self.cnx.commit()
                    
                    #print("AN")
                    
                    time.sleep(1)
                    #setze status in idnr_1 zu 1
                    self.mycursor.close()


            except:
            
                print("not enough entrys")
                
                
            
    def handler(self,signum,frame):
        print("time is over!")
        raise Exception("end of time") 
            
        

        #return modulliste
                        
    def main(self):
    
    
        try:
        
            #self.internet_on()
            self.bot = telegram.Bot(token=self.tokens)
           #self.mycursor = self.databaseconnectio()
            #print("test")
            self.send_keyboard()

        except:
            print("wrong start")
        
        signal.signal(signal.SIGALRM, self.handler)
            
        while True:


            try:

                signal.alarm(self.execution_timeout)
                
                #self.mycursor = self.databaseconnectio()
                self.bot = telegram.Bot(token=self.tokens)

                time.sleep(5)

                #self.module

                stepone = self.module()
                print("step1")
                steptwo = self.lastone(stepone)
                print("step2")
                self.auswertung(steptwo)
                print("finsish")

                #self.auswertung(self.lastone(self.module()))

                #self.mycursor.close()


                dt = datetime.datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                utc_timestamp_now = utc_time.timestamp()
                

                dt_string = str(utc_time.strftime("%d/%m/%Y %H:%M:%S"))
                print(dt_string)
                print(int(time.time()))

                with open("time.txt","a") as timestamp:
                    timestamp.write(""+str(int(time.time()))+"\n")

            except Exception as e:


                dt = datetime.datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                #utc_timestamp_now = utc_time.timestamp()

                #now = datetime.now()
                #dt_string = str(utc_timestamp_now)
                dt_string = str(utc_time.strftime("%d/%m/%Y %H:%M:%S"))
                with open("log.txt","a") as error:
                    error.write(""+dt_string+" stat "+str(e)+"\n")

                print(e)

                print("retry")
                
        

if __name__ == '__main__':
    objName = databasechatbot()
    objName.main()
    #pr1 = multiprocessing.Process(checkweb().main())
    #pr1.start()
    #pr1.join()

    #pr2 = multiprocessing.Process(databasechatbot().main())
    #pr1.start()
    #pr1.join()

    #webcheck = checkweb()
    #p2 = Process(target = webcheck.main())