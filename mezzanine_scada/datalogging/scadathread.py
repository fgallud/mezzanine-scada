# -*- coding: UTF-8 -*-
"""
This code saves all sensor values in real time every now and then. 
It saves the data into plain text files. One file for each day. This is usefull because is easy to reacue the data if the computer has an error.
It creates a directory for each year, inside it creates a directory for each month and inside it creates a file for each day

TODO list
- Wait for an event that become true when the database is created instead of waiting 60s
- Save the mean value instead of pick one value
- Export accecpting start and end times in different days. Warning, if the time range is too large, it can freeze the program. May be a week?
  maybe the correct way is in javascript to make a lot of ajax commands. If there are too many only the navigator page freeze, not the server
"""

import threading
import time
import os
import logging
from .models import *
from mezzanine_scada.base.models import variable

class scadathread(threading.Thread):
    def __init__(self,
                 database=None,
                 end=threading.Event(),
                 debug_logger=logging):       
        threading.Thread.__init__(self)  
        self.logger=debug_logger
        self.settings=datalogging.objects.first()
        self.stime=self.settings.sampling_time 
        self.path=self.settings.data_path
        self.database=database
        self.end=end
        #sensor list to be saved.
        self.sensor_name=[]
        self.sensor_gui=[]
        for sensor in variable.objects.all():
            self.sensor_name.append(sensor.name)
            self.sensor_gui.append(sensor.name_gui)
        self.mutex=threading.Semaphore()
    def run(self):
    #wait for the variable list to be made and with proper values (60segundos)
    #Every time it has to save a sample: 
    #    create the day file if it's not done yet
    #    save all sensors
        #wait 60s or until the app ends
        self.end.wait(60.0) 
        t0=time.time()
        t_next=t0
        while not self.end.isSet():
            t=time.localtime()
            file_name=os.path.join(self.path,'%04i' %t.tm_year)
            file_name=os.path.join(file_name,'%02i' %t.tm_mon)
            if not os.path.exists(file_name):
                os.makedirs(file_name)
            file_name=os.path.join(file_name,'%04i-%02i-%02i.dat' %(t.tm_year,t.tm_mon,t.tm_mday))
            if not os.path.exists(file_name):
                linea='fecha\thora'
                for s in self.sensor_gui:
                    linea=linea+'\t'+s
                self.mutex.acquire()
                f=open(file_name,'w')
                f.write(linea)
                f.close()
                self.mutex.release()
            linea='\r\n%02i-%02i-%04i\t%02i:%02i:%02i' %(t.tm_mday,t.tm_mon,t.tm_year,t.tm_hour,t.tm_min,t.tm_sec)
            for s in self.sensor_name:
                try:
                    tmp_value=self.database.get_value(name=s)['value']
                except:
                    tmp_value=-1.0
                linea=linea+'\t%f' %tmp_value
            self.mutex.acquire()
            f=open(file_name,'a')
            f.write(linea)
            f.close()
            self.mutex.release()
            #espear al proximo muestreo
            t_next=t_next+self.stime
            if time.time()>t_next:
                t_next=time.time()
            espera=t_next-time.time()
            if espera>0.0:
                self.end.wait(espera)
    def get_gui_name(self,name):
        for s,g in zip(self.sensor_name,self.sensor_gui):
            if s==name:
                return g
        return ''
    def export(self,start=0.0,end=0.0,names=[]):
    #this method accept a time since epoch as a start time, end time and a variable name list.
    #returns a dictionary with:
    #name and date are the same in all variables
    #a time field with the time since epoch 
    #a value field with the variable value 
    #start and end time must be in the same day
        data={}
        for n in names:
            data[n]={'time':[],'value':[]}
        t=time.localtime(start)
        #only in today file
        file_name=os.path.join(self.path,'%04i' %t.tm_year)
        file_name=os.path.join(file_name,'%02i' %t.tm_mon)
        file_name=os.path.join(file_name,'%04i-%02i-%02i.dat' %(t.tm_year,t.tm_mon,t.tm_mday))
        if not os.path.exists(file_name):
            logging.error("The file for the day %s doesn't exist" % file_name)
        else:
            #use the mutex in case it is the actual date
            self.mutex.acquire()
            f=open(file_name,'r')
            full_text=f.read()
            f.close()
            self.mutex.release()
            valores=full_text.split('\r\n')
            #the first line is a list of names
            valores=valores[1:]
            #if there isn't the correct amount of sensors in this line ignore
            valores_tmp=[]
            for iv in range(len(valores)):
                v_partido=valores[iv].split('\t')
                #is the time in the wanted range?
                try:
                    tiempo_str=v_partido[0]+'\t'+v_partido[1]
                    tiempo_epoch=time.mktime(time.strptime(tiempo_str, "%d-%m-%Y\t%H:%M:%S"))
                    if tiempo_epoch>start and len(v_partido)==(len(self.sensor_name)+2):
                        valores_tmp.append(v_partido)
                except:
                    pass
            valores=valores_tmp
            for l_partida in valores:
                t_line=l_partida[0]+'\t'+l_partida[1]
                try:
                    t_line=time.mktime(time.strptime(t_line, "%d-%m-%Y\t%H:%M:%S")) 
                except:
                    self.logger.error("Export: incorrect export time")
                    continue
                for n in names:
                    try:
                        valor=float(l_partida[2+self.sensor_name.index(n)])
                    except:
                        valor=-1.0
                        self.logger.error('Export: incorrect export time')
                    data[n]['time'].append(t_line)
                    data[n]['value'].append(valor) 
        return data





