# -*- coding: UTF-8 -*-
"""


"""
from filling_tank import filling_tank
import threading
import time
import os
import logging
from .models import *


class ServiceRoot:
    pass


class scadathread(threading.Thread):
    def __init__(self,
                 server=None,
                 database=None,
                 end=threading.Event(),
                 debug_logger=logging):       
        threading.Thread.__init__(self)  
        self.logger=debug_logger
        self.server=server
        self.database=database
        self.end=end
        self.thread_list={}
        for tank in filling_tank.objects.all():
            try:
                self.thread_list[tank.name]=filling_tank(database=database,
                                                         end=end,
                                                         debug_logger=debug_logger,
                                                         T=tank.state_time,
                                                         high_level_sensorr=tank.high_level_sensor.name,
                                                         bottom_level_sensor=tank.bottom_level_sensor.name,
                                                         filling_element=tank.filling_element.name)
                #expose the control methods on the xmlrpc server
                #this allows the gui to send commands to the state machine control
                #the system can have several controls so we need a dotted root to each of them
                controls = ServiceRoot()
                exec('controls.'+tank.name+' = self.thread_list[tank.name]')
                self.server.register_instance(exec('controls.'+tank.name),allow_dotted_names=True)
                #from clients we can now do proxy.tank_name.state_machine_method()
                #to call each state machine control methods                                           
            except:
                self.logger.error('SCADATHREAD: Error loading filling tank: %s' %tank.name)
                continue
    def run(self):
        for thread_name in self.thread_list:
            self.thread_list[thread_name].start()
        for thread_name in self.thread_list:
            self.thread_list[thread_name].join()

