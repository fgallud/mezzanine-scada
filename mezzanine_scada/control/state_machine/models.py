from django.db import models

"""
- a state machine is a array of states
- each state is:
    - state function
    - a init function
    - an end function
    - an array of transition conditions and functions


TODO list:
  - add alarms. The idea is to have a list of alarms set to tackle problems that can happen
  - an alarm is a function that returns a boolean that is true if the alarm is happening
  - each state machine have some alarms active througout the entire state machine and some
    that are only active on one state (or a few of them)
"""    
    
"""
class function(models.Model):
    name = models.CharField('Name of the function', max_length=150, default='')
    function_path = models.CharField('location of the function', max_length=300,default='.myapp.my_state_machine.my_library.my_function')
    description = models.CharField('descripcion', max_length=150,blank=True)
    function_code = models.TextField('code', max_length= 2000,blank=True,default='#function code\n#inside the state machine class\n\nself.databasereturn_value=False'
    def __str__(self):
        return '%s' %self.name

class alarm_condition(function):
#is a normal function but i don't want django admin to show all functions
#so  i need to change something 
    def __str__(self):
        return '%s alarm condition' %self.name

class alarm_action(function):
    def __str__(self):
        return '%s alarm action' %self.name

class alarm(models.Model):
    condition = models.ForeignKey(alarm_condition, null=True)
    action = models.ForeignKey(alarm_action, null=True)
#    variable = models.ForeignKey(variable)
#    minimum = models.FloatKey('Minimum value allowed')
#    maximum = models.FloatKey('Maximum value allowed')


class state_function(function):
    related_state = models.ForeignKey('state', blank=True, null=True)

class state(models.Model):
    name = models.CharField('Name of the function', max_length=150, default='')
    alarms = models.ManyToManyField(alarm,blank=True)
    function = models.ForeignKey(state_function, blank=True, null=True)
    def __str__(self):
        return '%s' %self.name

class init_function(function):
    state = models.ForeignKey(state, blank=True,null=True)

class transition_condition_function(function):
    origin_state =  models.ForeignKey(state,     related_name='condition_origin_state')
    destination_state = models.ForeignKey(state, related_name='condition_destination_state')


class transition_action_function(function):
    origin_state =  models.ForeignKey(state,     related_name='action_origin_state')
    destination_state = models.ForeignKey(state, related_name='action_destination_state')

class state_machine(models.Model):
    name = models.CharField('State machine name',max_length=100, default='')
    states = models.ManyToManyField(state)
    def __str__(self):
        return '%s' %self.name
    


"""


