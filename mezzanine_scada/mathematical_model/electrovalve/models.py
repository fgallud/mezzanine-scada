from django.db import models
from mezzanine_scada.base.models import variable


class electrovalve(models.Model):
    name = models.CharField('Name of the electrovalve',max_length=64)
    #variable that holds the flow in the line (whatever if the valve is open, 0 if it's closed)
    flow_variable = models.ForeignKey(variable,related_name='flow_variable')
    #variable that the user or whatever must write to open/close the valve
    input_variable = models.ForeignKey(variable,related_name='input_variable')
    def __str__(self):
        return '%s' %self.name


