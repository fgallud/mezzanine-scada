# -*- coding: UTF-8 -*-
"""
This is a template to create a new app in scada_mezzanine

The creation process is:

1.- Create an app with the command:
  python3 manage.py startapp my_app
  
3.- inside the app directory add the models wanted (if needed)

4.- copy the scadathread.py file to the directory.
    This file have a scadathread class that is a thread.
    the mezzanine_scada service daemon will load an runs this thread. 
    This thread work is to run all threads needed for this app and act as this app daemon
    Typically this thread will do task like:
      - read the value of a list of sensors every some time and update his value in the realtime database
      - wait a change in a variable in the realtime database and do some task like control, alarms, etc...
    this class accepts:
      - the realtime database that is used to save variable values, read them or wait until a variable value changes
      - the end event. The thread must end if this event becomes true
      - a logger to send info, error, debug,.. messages
5.- add this app to settings.py      

"""

import threading
import time
import os
import logging



class scadathread(threading.Thread):
    def __init__(self,
                 database=None,
                 end=threading.Event(),
                 debug_logger=logging):       
        threading.Thread.__init__(self)  
        self.logger=debug_logger
        self.database=database
        self.end=end
    def run(self):
        while not self.end.isSet():
            self.end.wait(60.0)
            print("I'm doing some important stuff")
