from django.db import models
import logging

class scada_config(models.Model):
    logging_file= models.CharField('path of the logging file',default='../scada.log')
    LOGGING_LEVELS = (
        (logging.FATAL, 'FATAL'),
        (logging.ERROR, 'ERROR'),
        (logging.WARN, 'WARN'),
        (logging.INFO, 'INFO'),
        (logging.DEBUG,'DEBUG'),
        (logging.TRACE, 'TRACE'),
    logging_level = IntegerField('Logging level',default=logging.DEBUG)
    
class variable(models.Model):
    CHANNEL_DIRECTION = (
        ('input','is a signal that is sampled'),
        ('output','is a signal that is generated'),
        ('dummy','is a signal without type'),
    )
    name = models.CharField('unique name of the variable', max_length=150)
    default_value = models.FloatField()
    direction = models.CharField('direction of the variable',max_length=20,choices=CHANNEL_DIRECTION)
    name_gui = models.CharField('name of the variable user friendly', max_length=150,blank=True)
    description = models.TextField('descripcion', max_length=150,blank=True)
    origin = models.TextField('description of the hardware that generate/measure this variable', max_length=150,blank=True)
    destination = models.TextField('What is this variable for?', max_length=150,blank=True)
    def __str__(self):
        return '%s:%s:%s' %(self.name,self.name_gui,self.direction)


class channel(variable):
    nchannel = models.PositiveIntegerField()
    def __str__(self):
        return '%i:%s:%s' %(self.nchannel,self.name,self.direction)


