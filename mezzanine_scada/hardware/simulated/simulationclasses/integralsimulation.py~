from time import time
from math import pi, sin

class simulationclass:
    def __init__(self, **kwargs):
        self.error=False
        if ('amplitude' not in kwargs) or ('frequency' not in kwargs) or ('phase' not in kwargs) or ('mean_value' not in kwargs):
            self.error=True
        else:
            self.amplitude=kwargs['amplitude']
            self.frequency=kwargs['frequency']
            self.phase=kwargs['phase']
            self.mean_value=kwargs['mean_value']
            self.database=kwargs['database']
            self.logger=kwargs['debug_logger']
            self.integral=0.0
            self.former_value=0.0
    
    def get_value(self):
        if self.error:
            return -1.0
        else:
            self.integral=self.integral+(time.time()-self.t0)
            return sin(2*pi*self.frequency*time()+self.phase)*self.amplitude+self.mean_value

