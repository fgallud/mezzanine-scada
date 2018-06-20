
class simulationclass:
    def __init__(self,**kwargs):
        if 'value' in kwargs:
            self.value=kwargs['value']
        else:
            self.value=-1.0
    
    def get_value(self):
        return self.value

