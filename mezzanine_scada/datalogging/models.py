from django.db import models

class datalogging(models.Model):
    sampling_time = models.FloatField('Sampling time [s]',default=60.0)
    data_path = models.CharField('Path where the data are saved',max_length=255)
    def __str__(self):
        return 'Data Logging Configuration'

