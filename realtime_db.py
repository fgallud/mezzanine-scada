# -*- coding: UTF-8 -*-
#así puedo usar letras no ascii estandar como áéíóúñ u otras

""" Este es una clase base de datos para señales


Para cada ficha de señal:
  nombre: texto para referirse a la señal. Es el nombre de la ficha, no un campo
  valor: ultimo valor conocido
  tiempo: tiempo en el cual la señal fue adquirida/generada (seg desde epoch)
  next: Un evento que se vuelve True cuando cambie el valor de la señal. 




metodos de la clase:
set_value(nombre,valor,tiempo) cambia (o añade si no existe una ficha)
get_value(nombre):       da un diccionario {'value':valor, 'time':valor}
                         donde value es el valor de la señal y time el tiempo en el que se adquirio/genero
get_value_next(nombre):  igual que get_last pero espera al proximo cambio de la señal.
                         El hilo que ejecuta esta funcion se bloqueará hasta que otro hilo
                         llame a set_value
get_multiple_value([nombres]) genera un vector de valores con los ultimos valores conocidos
get_multiple_value_next([nombres]) igual que get_multiple_value pero espera a nuevos valores
                                   esta funcion bloqueará el hilo hasta que algún otro hilo cambie los valores
                                   de las señales
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
    #cambia el valor de una señal y despierta a todos los que estuviesen esperando
    #si no existe la señal la crea
        try:
            value=float(value)
        except:
            return {'name':name,'value':-1.0,'time':t_aquisition,'error':True}
        if t_aquisition==0.0:
            t_aquisition=time.time()
        self.access.acquire()
        if name in self.data:
            self.data[name]['value']=value
            self.data[name]['time']=t_aquisition
        else:
            self.data[name]={'value':value,'time':t_aquisition,'waiting':threading.Event()}
        #ATENCION:hay que comprobar si entre el set y el clear se despierta a todos 
        self.access.release()
        self.data[name]['waiting'].set()
        self.data[name]['waiting'].clear()
        #al servirse este metodo por xmlrpc debe retornar algo
        return {'name':name,'value':value,'time':t_aquisition}
    
    def get_value(self,name=''):
    #retorna el ultimo valor conocido de la señal y el tiempo en que se obtuvo
        if name in self.data:
            self.access.acquire()
            try:
                tmp_value={'name':name, 'value':self.data[name]['value'], 'time':self.data[name]['time']}
            except:
                logging.error(self.name+' signal '+name+' does not exist')
                tmp_value={'name':name, 'value':-1,'time':0.0}
            self.access.release()
            return tmp_value
        else:
            return {'name':name, 'value':-1,'time':0.0}
    
    def get_value_next(self,name=''):
    #espera a que se actualice el valor de la señal y retorna valor y el tiempo en que se obtuvo
        if name in self.data:
            self.data[name]['waiting'].wait()
            return self.get_value(name)
        else:
            logging.error(self.name+' signal '+name+' does not exist')
            return {'value':-1,'time':0.0}
    
    def get_multiple_value(self,names=[]):
        data=[]
        for n in names:
            data.append(self.get_value(n))
        return data
    
    def get_multiple_value_next(self,names=[]):
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
    #se usa cuando se quiere terminar el programa, para que los hilos que
    #esten esperando salgan.
        self.access.release()
        for s in self.data:
            self.data[s]['waiting'].set()    
    
    def set_info(self,name='nombre del signal',name_gui=None,description=None):
        if name in self.data:
            self.access.acquire()
            try:
                if name_gui==None:
                    self.data[name]['name_gui']=name
                else:
                    self.data[name]['name_gui']=name_gui
                if description==None:
                    self.data[name]['description']=self.data[name]['name_gui']
                else:
                    self.data[name]['description']=description
            except:
                logging.error(self.name+' signal set_info error')
            self.access.release()
    
    def get_info(self,name='nombre del signal'):
        info={'name':name, 'name_gui':name,'description':name}
        if name in self.data:
            self.access.acquire()
            if 'name_gui' in self.data[name]:
                info['name_gui']=self.data[name]['name_gui']
            if 'description' in self.data[name]:
                info['description']=self.data[name]['description']
            self.access.release()
        return info         
