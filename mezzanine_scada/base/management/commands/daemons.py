# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from mezzanine_scada.base.database import variable_database
from mezzanine_scada.base.models import variable, scada_config

import time
import logging
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from xmlrpc.client import ServerProxy

from secrets import token_hex
from threading import Event, Thread
import daemon





class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def remote_shutdown():
    print("cerrando demonio")
    #python2.x -> thread.start_new_thread(shutdown_thread, ())
#    threading.Thread(target=shutdown_thread).start()
    return 'Returned from remote_shutdown'


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
        print("tirando abajo el demonio")
        if password==self.server_pasword:
            print(1)
            self.end_event.set()
            print(2)
            for thread_name in self.thread_list:
                try:
                    print(3)
                    self.thread_list[thread_name].join(10.0)
                    print(thread_name+" ended")
                except:
                    message="ERROR: "+thread_name+" can't exit"
                    print(message)
                    self.logger.error(message)
            self.logger.error("saliendo del servidor xmlrpc") 
            #falta terminar el servidor xmlrpc
    
    def stop(self):
        #conect with the server and end the daemon
        try:
            #it should use https if this is going to be on the internet
            proxy = ServerProxy('http://localhost:%i' %self.settings.server_port)
            proxy.remote_shutdown()#shutdown_daemon(self.server_password)
        except:
            message="DAEMON can't stop"
            print(message)
            self.logger.error(message)
    
    def start(self):
        #the password is one use only
        self.settings.server_password=token_hex(16)
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
            self.realtime_db.set_value(name=var.name,value=var.default_value,t_aquisition=time.time())
        #execute all threads needed
        #thread for saving variable values to files
        #hardware related threads
        #one thread for each output variable
        #one thread for each input type of hardware
        #control related threads
        #a xmlrpc server to be able to access methods from outside this process
        #this should use https if it is going to be in a unsafe net
        self.server = SimpleXMLRPCServer(("localhost", self.settings.server_port),
                                          requestHandler=RequestHandler)
        self.server.register_introspection_functions()
#        self.server.register_function(self.shutdown_daemon, "shutdown_daemon")
        self.server.register_function(pow, "pow")
        self.server.register_function(remote_shutdown, "remote_shutdown")
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
            scada.start()
        elif 'stop' == options['action'][0]:
            scada.stop()

"""
This version can execute start as a daemon. Use this if you want a command that can load the daemon at his own
Is better a non daemonized version and use systemd to daemonize the thread

#daemonized version
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
 

"""

    

