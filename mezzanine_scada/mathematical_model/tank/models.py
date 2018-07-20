from django.db import models
from mezzanine_scada.base.models import variable



class tank(models.Model):
    name = models.CharField('Name of the tank',max_length=64)
    maximum_volume = models.FloatField() #maximum volume allowed
    initial_volume = models.FloatField() #volume at the begining
    volume = models.ForeignKey(variable,related_name='volume')
    input_flow = models.ForeignKey(variable,related_name='input_flow')
    output_flow = models.ForeignKey(variable,related_name='output_flow')
    loop_time = models.FloatField()
    def __str__(self):
        return '%s' %self.name



