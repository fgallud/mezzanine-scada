# -*- coding: UTF-8 -*-
from threading import Event
from mezzanine_scada.base.database import variable_database
from mezzanine_scada.base.models import variable
from time import time

#an event that makes all daemon to stop
end_event=Event()

#realtime database instance
realtime_db=variable_database(name='Data Base')
#pre-create all variables
for var in variable.objects.all():
    realtime_db.set_value(name=var.name,value=var.default_value,t_aquisition=time())

#one thread for every output variable. This thread waits for a change in the variable and then it sends the new value to the real world
#for var in variable.objects.filter(direction='output'):
#    new_thread=output_variable_thread(instrument=output_channels[signal_name]['driver'],
#                              database=realtime_db,
#                              name=signal_name,
#                              nchannel=output_channels[signal_name]['nchannel'],
#                              end=end_event,
#                              debug_logger=logger)
