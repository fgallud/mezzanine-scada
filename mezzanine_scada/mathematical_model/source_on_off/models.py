from django.db import models
from mezzanine_scada.base.models import variable

#this class is used to simulate a source of flow in witch 
#the source provide a constant flow if the source is on and
#another flow if it's off
#It can be a pump, a valve or something similar.
class source_on_off(models.Model):
    name = models.CharField('Name of the source',max_length=64,help_text='name of the source')
    flow_off = models.FloatField('flow if it is off')
    flow_on = models.FloatField('flow if it is on')
    flow_variable = models.ForeignKey(variable,related_name='flow_variable',help_text='the app will save the value of the flow in this variable in the realtime database')
    input_variable = models.ForeignKey(variable,related_name='input_variable',help_text='the source is on when someone writes 1.0 in this variable, off if 0.0')
    def __str__(self):
        return '%s' %self.name




