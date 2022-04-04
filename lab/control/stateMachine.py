import random
import control.config as config
from transitions import Machine

class thermostat:

    STATESLIST = ['start', 'warming', 'cooling', 'off', 'changing']

    def __init__(self, id):
        self.machine = Machine(model=self, states=thermostat.STATESLIST, initial ='start')
        self.temp = config.start_temp
        self.target = config.start_target
        self.temp_max = config.start_temp_max
        self.temp_min = config.start_temp_min
        self.id = 'TH'+str(id)
        self.target = config.start_target
        self.last_state = 'warming'
        self.target_dist = config.initial_cero
        self.power = config.initial_one
        self.last_target = config.start_target

        self.machine.add_transition(trigger='initialize', source='start', dest='warming')
        self.machine.add_transition(trigger='start_cooling', source=['warming','changing'], dest='cooling')
        self.machine.add_transition(trigger='start_warming', source=['cooling','changing'], dest='warming')
        self.machine.add_transition(trigger='target_changing', source='*', dest='changing')

        self.machine.add_transition(trigger='power_off', source='*', dest='off')
        self.machine.add_transition(trigger='power_on', source='off', dest=self.last_state)


