from django.db import models

"""
models for the detection and treatment of alarm situations.

"""    
    

class alarm_function(models.Model):
    name = models.CharField('Name of the function', max_length=150, default='')
    function_path = models.CharField('location of the function', max_length=300,default='.myapp.my_state_machine.my_library.my_function')
    description = models.TextField('descripcion', max_length=150,blank=True)
    def __str__(self):
        return '%s' %self.name

class alarm_condition(alarm_function):
#is a normal function but i don't want django admin to show all functions
#so  i need to change something 
    def __str__(self):
        return '%s alarm condition' %self.name

class alarm_action(alarm_function):
    def __str__(self):
        return '%s alarm action' %self.name

class alarm(models.Model):
    condition = models.ForeignKey(alarm_condition, null=True)
    action = models.ForeignKey(alarm_action, null=True)
#    variable = models.ForeignKey(variable)
#    minimum = models.FloatKey('Minimum value allowed')
#    maximum = models.FloatKey('Maximum value allowed')

