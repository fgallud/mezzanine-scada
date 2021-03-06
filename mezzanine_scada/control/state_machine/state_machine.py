#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Esta librería genera automatas de states. 
Para trabajar con esta librería se sigue este proceso:
- Crear una clase para construir el automata
- Registrar los states con su function de state que se ejecutan cada Tm tiempo mientras se esté en un state determinado
- Registrar functiones de condición que dan true si hay que pasar de un state a otro
- Registrar las functiones de inicio que se ejecutan solo una vez al pasar de cualquier state a uno A
- Registrar las functiones de finalización que se ejecutan solo una vez, al pasar del state A a cualquier otro
- Registrar las functiones de transición que se ejecutan solo una vez al pasar de un state A a otro B

El automata sigue este procedimiento

  Mientras no se pase a otro state, se ejecuta la function de state cada Tm segundos, luego se ejecutan todas las functiones de condición y la primera que da True genera una transición a otro state.

  Al pasar de un state A a otro B se ejecuta primero la function de finalización del state A, luego la función de transición del state A al B, luego la función de inicio del state B y finalmente se inicia el bucle que ejecuta la function del state B cada T tiempo
 

Ejemplo para crear un state

#functiones de state
def state_A(): print 'state A'

def state_B(): print 'state B'

def state_C(): print 'state C'

#variables globales para hacer que pase de un state a otro
AB=False
AC=False
BA=False
BC=False
CA=False
CB=False
#functiones de condicion
def condicion_AB(): return AB

def condicion_AC(): return AC

def condicion_BA(): return BA

def condicion_BC(): return BC

def condicion_CA(): return CA

def condicion_CB(): return CB

#functiones de inicio 
def inicio_A(): print 'inicio A'

def inicio_B(): print 'inicio B'

def inicio_C(): print 'inicio C'

#functiones de finalizacion 
def finalizacion_A(): print 'finalizacion A'

def finalizacion_B(): print 'finalizacion B'

def finalizacion_C(): print 'finalizacion C'

#functiones de transicion
def transicion_AB(): print 'transicion A a B'

def transicion_AC(): print 'transicion A a C'

def transicion_BA(): print 'transicion B a A'

def transicion_BC(): print 'transicion B a C'

def transicion_CA(): print 'transicion C a A'

def transicion_CB(): print 'transicion C a B'

#crea la clase que ejecuta el automata de states
import logging
import threading
import time
import logging

evento_salir=threading.Event()
automata=automata_monohilo(T=10.0,debug_logger=logging,end=evento_salir)
#crea los states
automata.register_state(name='A',function=state_A)
automata.register_state(name='B',function=state_B)
automata.register_state(name='C',function=state_C)
#registra las functiones de condicion
automata.register_condition(source='A',destination='B',function=condicion_AB)
automata.register_condition(source='A',destination='C',function=condicion_AC)
automata.register_condition(source='B',destination='A',function=condicion_BA)
automata.register_condition(source='B',destination='C',function=condicion_BC)
automata.register_condition(source='C',destination='A',function=condicion_CA)
automata.register_condition(source='C',destination='B',function=condicion_CB)
automata.register_init(state='A',function=inicio_A)
automata.register_init(state='B',function=inicio_B)
automata.register_init(state='C',function=inicio_C)
automata.register_end(state='A',function=finalizacion_A)
automata.register_end(state='B',function=finalizacion_B)
automata.register_end(state='C',function=finalizacion_C)
automata.register_transition(source='A',destination='B',function=transicion_AB)
automata.register_transition(source='A',destination='C',function=transicion_AC)
automata.register_transition(source='B',destination='A',function=transicion_BA)
automata.register_transition(source='B',destination='C',function=transicion_BC)
automata.register_transition(source='C',destination='A',function=transicion_CA)
automata.register_transition(source='C',destination='B',function=transicion_CB)
automata.initial_state('A')
automata.start()



"""


import threading
import time
import logging

#base state machine class
class state_machine(threading.Thread):
    def __init__(self,
                 T=60.0,
                 end=threading.Event(),
                 debug_logger=logging):       
        threading.Thread.__init__(self)
        self.__rlock=threading.RLock()
        self.tm=T
        self.logger=debug_logger
        self.end=end
        self.tn_1=time.time()
        self.current_state=''
        self.states={}
    def acquire(self):
        self.__rlock.acquire()
    def release(self):
        self.__rlock.release()
    def __register_state(self,name='estate A',function=None):
        self.states[name]={'name':name,
                              'state_function':function,
                              'condition_functions':{},
                              'init_function':None,
                              'end_function':None,
                              'transition_functions':{}}
    def register_state(self,name='estate A',function=None):
        self.acquire()
        self.__register_state(name=name,function=function)
        self.release()
    def __register_condition(self,source='estate A',destination='estate B',function=None):
        self.states[source]['condition_functions'][destination]={'source':source,
                                                              'destination':destination,
                                                              'function':function}
    def register_condition(self,source='estate A',destination='estate B',function=None):
        self.acquire()
        self.__register_condition(source=source,destination=destination,function=function)
        self.release()
    def __register_init(self,state='estate A',function=None):
        self.states[state]['init_function']=function
    def register_init(self,state='estate A',function=None):
        self.acquire()
        self.__register_init(state=state,function=function)
        self.release()
    def __register_end(self,state='state A',function=None):
        self.states[state]['end_function']=function
    def register_end(self,state='state A',function=None):
        self.acquire()
        self.__register_end(state=state,function=function)
        self.release()
    def __register_transition(self,source='state A',destination='state B',function=None):
        self.states[source]['transition_functions'][destination]={'source':source,
                                                               'destination':destination,
                                                               'function':function}
    def register_transition(self,source='state A',destination='state B',function=None):
        self.acquire()
        self.__register_transition(source=source,destination=destination,function=function)
        self.release()
    def __change_state(self,destination='state destination'):
        try:
            self.states[self.current_state]['end_function']()
        except:
            pass
        try:
            self.states[self.current_state]['transition_functions'][destination]['function']()
        except:
            pass
        try:
            self.states[destination]['init_function']()
        except:
            pass
        self.current_state=destination
        return destination
    def change_state(self,destination='state destination'):
        self.acquire()
        returned_value=self.__change_state(destination=destination)
        self.release()
        return returned_value
    def __get_state(self):
        return self.current_state
    def get_state(self):
        self.acquire()
        returned_value=self.__get_state()
        self.release()
        return returned_value
    def __set_state_time(self,tm=60.0):
        self.tm=tm
    def set_state_time(self,tm=60.0):
        self.acquire()
        self.__set_state_time(tm=tm)
        self.release()
        return returned_value
    def __change_initial_state(self,state='state A'):
        self.initial_state=state
    def change_initial_state(self,state='state A'):
        self.acquire()
        self.__change_initial_state(state=state)
        self.release()
    def __wait_state(self):
        now_time=time.time()
        wait_time=max(0.0,self.tn_1+self.tm-now_time)
        time.sleep(wait_time)
        self.tn_1=now_time+wait_time
    def run(self):
        self.acquire()
        try:
            self.states[self.initial_state]['init_function']()
        except:
            pass
        self.current_state=self.initial_state
        while not self.end.is_set():
            self.states[self.current_state]['state_function']()
            #I let other threads to interact with this thread
            self.release()
            self.__wait_state() 
            self.acquire()
            #It's time for a transition?
            for destination in self.states[self.current_state]['condition_functions']:
                if self.states[self.current_state]['condition_functions'][destination]['function'](): 
                #if the function is None, It works
                    #It's going to do a transition
                    self.__change_state(destination)
                    break
        self.release()




