from django.db import models
from mezzanine_scada.base.models import variable
from mezzanine_scada.mathematical_model.tank.models import tank


class float_sensor(models.Model):
    SWITCH_LOGIC_CHOICES = (
        (True, 'The float sensor is true when the level reach the sensor level'),
        (False, 'The float sensor is false when the level reach the sensor level'),
    )
    name = models.CharField('Name of the float sensor',max_length=64)
    tank = models.ForeignKey(tank,related_name='tank')
    switch_volume = models.FloatField() #if the tank volume reach this level, the float sensor will change its status
    switch_logic = models.BooleanField(choices=SWITCH_LOGIC_CHOICES) 
    output_var = models.ForeignKey(variable,related_name='output_var',help_text='variable in witch is the output of this sensor')
    def __str__(self):
        return '%s' %self.name


