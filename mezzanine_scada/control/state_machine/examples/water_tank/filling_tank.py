# -*- coding: UTF-8 -*-


import time
from mezzanine_scada.control.state_machine.state_machine import state_machine

class filling_tank(state_machine):
    def __init__(self,
                 database=None,        
                 end=None,
                 debug_logger=logging,
                 T=9.0,
                 high_level_sensor='din_level_input_nomal_up',
                 high_level_active_value=1.0,
                 bottom_level_sensor='din_level_input_normal_bottom',
                 bottom_level_active_value=0.0,
                 filling_element='dout_valve_input'):
        state_machine.__init__(self,
                               T=T,
                               end=end,
                               debug_logger=debug_logger)
        self.high_level_sensor=high_level_sensor
        self.bottom_level_sensor=bottom_level_sensor
        if high_level_active_value:
            self.high_level_active_value=1.0
        else:
            self.high_level_active_value=0.0
        if bottom_level_active_value:
            self.bottom_level_active_value=1.0
        else:
            self.bottom_level_active_value=0.0
        self.filling_element=filling_element
        self.register_state(name='manual_on',function=self.state_manual_on)
        self.register_state(name='manual_off',function=self.state_manual_off)
        self.register_state(name='auto_filling',function=self.state_auto_filling)
        self.register_state(name='auto_filled',function=self.state_auto_filled)
        self.change_initial_state(state='manual_off')
        self.register_condition(source='auto_filling',destination='auto_filled',function=self.condition_filling_to_filled)
        self.register_condition(source='auto_filled',destination='auto_filling',function=self.condition_filled_to_filling)
    #state functions
    def state_manual_on(self):
        self.database.set_value(self.filling_element,1.0)
    def state_manual_off(self):
        self.database.set_value(self.filling_element,0.0)
    def state_auto_filling(self):
        time.sleep(0.1)
        self.database.set_value(self.filling_element,1.0)
        time.sleep(0.1)
    def state_auto_filled(self):
        time.sleep(0.1)
        self.database.set_value(self.filling_element,0.0)
        time.sleep(0.1)
    #functiones de condicion de cambio de state
    def condition_filling_to_filled(self):
        return self.database.get_value(self.high_level_sensor)['value']==self.high_level_active_value
    def condition_filled_to_filling(self):
        return self.database.get_value(self.bottom_level_sensor)['value']==self.bottom_level_active_value






