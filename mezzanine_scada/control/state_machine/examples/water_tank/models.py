from django.db import models
from mezzanine_scada.base.models import variable

# Create your models here.
class filling_tank(models.Model):
    state_time = models.FloatField(default=10.0)
    high_level_sensor= models.ForeignField(variable)
    high_level_active_value= models.BooleanField(default=True)
    bottom_level_sensor= models.ForeignField(variable)
    bottom_level_active_value = models.BoobleanField(default=False)
    filling_element=  models.ForeignField(variable)
    