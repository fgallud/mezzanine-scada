# -*- coding: UTF-8 -*-

""" 
This is a class to deal with all the variables in the system.
Main features needed:
  - multithread safe
  - a thread can wait until a variable changes his value
  - contains value and time at witch was the last change
  
Every variable has properties:
  name: string that identify the variable. It has to be unique across the database.
  value: Last known value. Is a float value.
  time: is the time at witch the value was changed the last time. The format is in seconds since epoch.
  next: An event. If a thread waits with this event, It will wake up when the value will change.

Methods:
  set_value(name,value,time) This method changes the value of the variable.
get_value(nombre):       returns a dictionary with: 'value':value, 'time':time}
                         where value is the value of the variable and time is the time in seconds since epoch when it was changed.
                         this method does not wait
get_value_next(nombre):  It is the same than the later but it waits until the next change of the variable.
                         If a thread calls this method, it will sleep until some other thread will call to set_value for this variable.
get_multiple_value([name1,...]) this generates an array of dictionaries with the last known value of the variables asked.
get_multiple_value_next([name1,...]) Its the same than the later but it waits until all the variables will change
"""

import threading
import logging
import time

class signal_database:
    def __init__(self,name='Data Base'):
        self.name=name
        self.data={}
        self.access=threading.Semaphore()
    
    def set_value(self,name='',value=0.0,t_aquisition=0.0):
        try:
            value=float(value)
        except:
            return {'name':name,'value':float('nan'),'time':t_aquisition,'error':True}
        if t_aquisition==0.0:
            t_aquisition=time.time()
        self.access.acquire()
        if name in self.data:
            self.data[name]['value']=value
            self.data[name]['time']=t_aquisition
        else:
            #first time. Create the variable
            self.data[name]={'value':value,'time':t_aquisition,'waiting':threading.Event()}
        self.access.release()
        #wake up all the threads that call get_value_next
        self.data[name]['waiting'].set()
        self.data[name]['waiting'].clear()
        return {'name':name,'value':value,'time':t_aquisition}
    
    def get_value(self,name=''):
        if name in self.data:
            self.access.acquire()
            try:
                tmp_value={'name':name, 'value':self.data[name]['value'], 'time':self.data[name]['time']}
            except:
                logging.error(self.name+' signal '+name+' does not exist')
                tmp_value={'name':name, 'value':float('nan'),'time':0.0}
            self.access.release()
            return tmp_value
        else:
            return {'name':name, 'value':float('nan'),'time':0.0}
    
    def get_value_next(self,name=''):
        if name in self.data:
            self.data[name]['waiting'].wait()
            return self.get_value(name)
        else:
            logging.error(self.name+' signal '+name+' does not exist')
            return {'value':float('nan'),'time':0.0}
    
    def get_multiple_value(self,names=[]):
        data=[]
        for n in names:
            data.append(self.get_value(n))
        return data
    
    def get_multiple_value_next(self,names=[]):
    #maybe its better to wait for one variable and then check the time on the others these are to much threads
        threads=[]
        for n in names:
            if n in self.data:
                event=self.data[n]['waiting']
                thread=threading.Thread(target=event.wait)
                thread.start()
                threads.append(thread)
            else:
                logging.error(n+' is not a member of the signal database')
        for t in threads:
            t.join()
        return self.get_multiple_value(names)
    
    def get_allnames(self):
        name_list=[]
        self.access.acquire()
        for name in self.data:
            name_list.append(name)
        self.access.release()
        return name_list
    
    def set_all_events(self):
    #this is used when we whant to end the program. This wake up all the threads.
        self.access.release()
        for s in self.data:
            self.data[s]['waiting'].set()    


#The gui name is better in the django database.
#    def set_info(self,name='nombre del signal',name_gui=None,description=None):
#        if name in self.data:
#            self.access.acquire()
#            try:
#                if name_gui==None:
#                    self.data[name]['name_gui']=name
#                else:
#                    self.data[name]['name_gui']=name_gui
#                if description==None:
#                    self.data[name]['description']=self.data[name]['name_gui']
#                else:
#                    self.data[name]['description']=description
#            except:
#                logging.error(self.name+' signal set_info error')
#            self.access.release()
#    
#    def get_info(self,name='nombre del signal'):
#        info={'name':name, 'name_gui':name,'description':name}
#        if name in self.data:
#            self.access.acquire()
#            if 'name_gui' in self.data[name]:
#                info['name_gui']=self.data[name]['name_gui']
#            if 'description' in self.data[name]:
#                info['description']=self.data[name]['description']
#            self.access.release()
#        return info         
