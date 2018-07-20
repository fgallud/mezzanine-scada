# -*- coding: UTF-8 -*-
"""
This app allow us to simulate a tank. This tank have a maximum volume, a initial volume 
an input flow and an output flow that would be two variables.

we can use other mathematical models with this one like level sensors that will change with the volume of the tank, valves or pumps
that will modify the input or output flow, ...



"""



import threading
import logging
from .models import *
from tank import *



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
        for var_tank in tank.objects.all():
            try:
                tank_instance=tank_simulator(database=self.database,
                                             end=self.end,
                                             logger=self.logger,
                                             tank_maximum_volume=var_tank.maximum_volume,
                                             tank_volume_name=var_tank.volume.name, 
                                             tank_initial_volume=var_tank.initial_volume,
                                             input_flow_name=var_tank.input_flow.name,
                                             output_flow=var_tank.output_flow.name,
                                             loop_time=var_tank.loop_time)
                self.thread_list[var_tank.name]=tank_instance
            except:
                self.logger.error('Error creating tank: %s' %var_tank.name)
                continue
    def run(self):
        for thread_name in self.thread_list:
            self.thread_list[thread_name].start()
        for thread_name in self.thread_list:
            self.thread_list[thread_name].join()


