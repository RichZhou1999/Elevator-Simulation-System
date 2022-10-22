import numpy as np
'''

state: wait or running

'''


class Elevator:
    def __init__(self, capacity, max_speed, name, acceleration):
        self._capacity = capacity
        self._max_speed = max_speed
        self.cur_speed = 0
        self.acceleration = acceleration
        self.current_accommodation = 0
        self.current_height = 0
        self._state = "run"
        self.cur_waited_time = 0
        self.destination_floor = None
        self._direction = None
        self.request_floor_list = []
        self.current_passenger_list = []
        self.name = name
    @property
    def state(self):
        return self._state

    @property
    def capacity(self):
        return self._capacity

    @property
    def max_speed(self):
        return self._max_speed

    @property
    def direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def set_state(self, state):
        self._state = state

    def update(self, simulation_step, **kwargs):
        self.adjust_acceleration(acceleration=kwargs["acceleration"])
        self.adjust_height(simulation_step)
        self.adjust_speed(simulation_step)
        self.adjust_request_floor_list()

    def adjust_request_floor_list(self):
        for passenger in self.current_passenger_list:
            self.request_floor_list[passenger.destination_floor] = 1

    def adjust_acceleration(self, acceleration):
        self.acceleration = acceleration
        if acceleration > 0:
            self.set_direction("up")
        elif acceleration < 0:
            self.set_direction("down")

    def adjust_speed(self, simulation_step):
        self.cur_speed += self.acceleration * simulation_step
        if abs(self.cur_speed) > abs(self.max_speed):
            self.cur_speed = self.max_speed * abs(self.cur_speed)/self.cur_speed


    def adjust_height(self, simulation_step):
        self.current_height = self.current_height +\
                              self.cur_speed * simulation_step + self.acceleration/2*simulation_step**2


