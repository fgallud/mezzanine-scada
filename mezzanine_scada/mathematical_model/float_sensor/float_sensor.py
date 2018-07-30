from threading import Thread, Event
from time import time
from math import isnan
import logging


def xnor(a,b):
    return not a ^ b



#thread that simulates a real world source
class float_sensor_simulator(Thread):
#This class simulates the behavior of a float sensor.
#the thread must wait until the level of a tank changes and
#if the level of the tank reaches certein level it changes the value
#to 1.0 or 0.0
#if the switch_logic is true, then the output is true if the level is bigger than the switch level
#if the switch_logic is false, the logic is inverted
#
#logic function = XOR
#
#switch_logic     current_level>switch_level   out
#     0                        0                1
#     0                        1                0
#     1                        0                0
#     1                        1                1
# 
    def __init__(self, 
                   database=None,
                   end=None,
                   logger=logging,
                   switch_volume = 0.0,
                   switch_logic=True,  #if true, the float sensor is true when the level is bigger than the switch volume
                   level_var='the_name_of_the_level_in_the_database',
                   output_var='the_name_of_the_output_var_in_the_database'):        
        Thread.__init__(self)
        self.database=database
        self.end=end
        self.logger=logger
        self.switch_volume=switch_volume
        self.switch_logic=bool(switch_logic)
        self.current_level_name=level_var
        self.output_name=output_var
        self.set_state(self.database.get_value(name=self.current_level_name)['value'])
    
    def set_state(self,level=0.0):
        self.current_level=level
        try:
            new_output=float(xnor(self.current_level>self.switch_volume,self.switch_logic))
        except:
            pass
        self.set_value(name=self.output_name,value=new_output)
      
      def run(self):
      #there is anything to do until the input variable changes
          while not self.end.isSet():
              #wait until the input variable changes
              level=self.database.get_value_next(name=self.current_level_name)['value']
              if isnan(level):
                  continue
              self.set_state(level)




