from threading import Thread, Event
from time import time
from math import isnan
import logging

#thread that simulates a real world source
class source_on_off_simulator(Thread):
#This class simulates the behavior of a source. 
#the flow output of the source is constant unless the input variable change
#if the input variable is 0.0 the flow is a constant and
#if the input variable is 1.0 the flow is another.
    def __init__(self, 
                 database=None,
                 end=None,
                 logger=logging,
                 flow_off=0.0,
                 flow_on=0.0,
                 input_var='my_digital_control_var',
                 flow_var='my_output_flow',
                 init_state=0.0):                            #state of the input_var at the beggining  
        Thread.__init__(self)
        print('en __init__ de source_on_off_simulator')
        self.database=database
        self.end=end
        self.logger=logger
        self.flow_off=flow_off
        self.flow_on=flow_on
        self.input_var=input_var
        self.flow_var=flow_var
        self.flow_current=0.0
        print('a')
        v=self.database.get_value(name=self.input_var)
        print('aa')
        print(v)
        self.set_state(value=self.database.get_value(name=self.input_var)['value'])
        print('b')
        self.database.set_value(name=self.input_var,value=init_state)
        print('fin de __init__ source_on_off_simulator')
    
    def set_state(self,value=0.0):
        print(value)
        self.state=bool(value)
        print(self.state)
        if self.state:
            #set state to on
            print('a on')
            self.flow_current=self.flow_on
        else:
            #set state to off
            print('a off')
            print(self.flow_off)
            self.flow_current=self.flow_off
            print('fin off')
        print('flow pasa a %f' %self.flow_current)
        self.database.set_value(name=self.flow_var,value=self.flow_current)
        print('fin de state')
    
    def run(self):
    #there is anything to do until the input variable changes
        print('running source_on_off run loop')
        while not self.end.isSet():
            #wait until the input variable changes
            input_value=self.database.get_value_next(name=self.input_var)['value']
            print('input_value = %f' %input_value)
            if isnan(input_value):
                continue
            self.set_state(input_value)




