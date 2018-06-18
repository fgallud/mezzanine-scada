# -*- coding: UTF-8 -*-
from threading import Event, Thread
from mezzanine_scada.base.database import variable_database
from mezzanine_scada.base.models import variable, scada_config
from time import time, sleep
import logging
from django.core.management.base import BaseCommand
from ssl import SSLContext
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from secrets import token_hex

import sys
import time

import daemon





class ScadaDaemon:
    def __init__(self):
        self.settings=scada_config.objects.first()
        logging.basicConfig(level=self.settings.logging_level,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename=self.settings.logging_file,
                            filemode='w')
        self.logger=logging 
    
    def shutdown_daemon(self, password):
        #this is the stop routine running in the daemon context
        #end all threads
        if password==self.server_pasword:
            self.end_event.set()
            for thread_name in self.thread_list:
                try:
                    self.thread_list[thread_name].join(10.0)
                    print(thread_name+" ended")
                except:
                    message="ERROR: "thread_name+" can't exit"
                    print(message)
                    self.logger.error(message)
            self.logger.error("saliendo del servidor xmlrpc") 
            #falta terminar el servidor xmlrpc
    
    def add(self,x,y):
        return x+y
    
    def stop(self):
        #conect with the server and end the daemon
        try:
            proxy=ServerProxy('https://localhost:%i/' %self.settings.server_port)
            proxy.shutdown_daemon(self.server_password)
        except:
            message="DAEMON can't stop"
            print(message)
            self.logger.error(message)
    
    def start(self):
        #the password is one use only
        self.settings.password=token_hex(16)
        self.settings.save()
        #create all instances and run all threads
        #a dictionary of threads that are executing
        thread_list={}
        #this event ends the daemon
        self.end_event=Event()
        #realtime database instance
        self.realtime_db=variable_database(name='Data Base')
        #pre-create all variables
        for var in variable.objects.all():
            self.realtime_db.set_value(name=var.name,value=var.default_value,t_aquisition=time())
        #execute all threads needed
        #thread for saving variable values to files
        #hardware related threads
        #one thread for each output variable
        #one thread for each input type of hardware
        #control related threads
        #a xmlrpc server to be able to access methods from outside this process
        context = SSLContext()
        self.server = SimpleXMLRPCServer(("https://localhost", SERVER_PORT),context=context)
        self.server.register_function(shutdown_daemon, "shutdown_daemon")
        self.server.register_function(add, "add")
        #serve_forever waits forever, only the call to the inherited shutdown method from another thread can stop it
        self.server.serve_forever()


class Command(BaseCommand):
    help = 'command that load all threads in mezzanine-scada'
    def add_arguments(self, parser):
        parser.add_argument('action', choices=['start', 'stop'], nargs='+', type=str)
    def handle(self, *args, **options):
        #service instance
        scada = ScadaDaemon()
        if 'start' == options['action'][0]:
            with daemon.DaemonContext():
                scada.start()
        elif 'stop' == options['action'][0]:
            scada.stop()
 



    

