from django.db import models
from mezzanine_scada.base.models import variable




class simulated_variable(variable):
    simulation_class = models.CharField(max_length=400, null=False, blank=False,help_text="is the class path where the simulationclass is in",default='mezzanine_scada.hardware.simulated.simulatedclasses.constantsimulation')
    simulation_class_kwargs = models.CharField(null=False, blank=False, default='',max_length=400,
                                               help_text='''arguments in json format for the class. {"value":1.0 } for instance''')
    sampling_time = models.FloatField('Sampling time',default=10.0)
    def __str__(self):
        return self.name


