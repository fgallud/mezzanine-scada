# -*- coding: UTF-8 -*-
"""
This app allow us to simulate a tank. This tank have a maximum volume, a initial volume 
an input flow and an output flow that would be two variables.

we can use other mathematical models with this one like level sensors that will change with the volume of the tank, valves or pumps
that will modify the input or output flow, ...



"""



import threading
import logging
from .models import float_sensor
from .float_sensor import float_sensor_simulator



class scadathread(threading.Thread):
    def __init__(self,
                 server=None,
                 database=None,
                 end=threading.Event(),
                 debug_logger=logging):       
        threading.Thread.__init__(self)  
        self.logger=debug_logger
        self.database=database
        self.end=end
        self.thread_list={}
        for var_float in float_sensor.objects.all():
            try:
                float_sensor_instance=float_sensor_simulator(database=self.database,
                                                             end=self.end,
                                                             logger=self.logger,
                                                             switch_volume = var_float.switch_volume,
                                                             switch_logic= var_float.switch_logic,
                                                             level_var= var_float.tank.volume,
                                                             output_var= var_float.output_var.name)
                self.thread_list[var_float.name]=float_sensor_instance
            except:
                self.logger.error('Error creating float sensor: %s' %var_float.name)
                continue
    def run(self):
        for thread_name in self.thread_list:
            self.thread_list[thread_name].start()
        for thread_name in self.thread_list:
            self.thread_list[thread_name].join()


