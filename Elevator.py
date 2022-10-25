import numpy as np
'''

state: wait or run

'''


class Elevator:
    def __init__(self, capacity, max_speed, name, max_acceleration):
        self._capacity = capacity
        self._max_speed = max_speed
        self.cur_speed = 0
        self.max_acceleration = max_acceleration
        self.acceleration = 0
        self.current_accommodation = 0
        self.current_height = 0
        self._state = "run"
        # current wait time of one elevator in a single floor
        self.cur_waited_time = 0
        self.destination_floor = None
        self._direction = "up"
        # the buttons pressed in the elevator, i.e. if passenger want to go 3th floor, list[3] = 1
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

    # update h,v,a information of elevator
    def update(self, simulation_step, **kwargs):
        self.adjust_height(simulation_step)
        self.adjust_speed(simulation_step)
        self.adjust_request_floor_list()
        self.adjust_acceleration(acceleration=kwargs["acceleration"])
        print("speed:", self.cur_speed)

    def adjust_request_floor_list(self):
        # set the list[floor] equals to 1 if inner passenger want to go
        for passenger in self.current_passenger_list:
            self.request_floor_list[passenger.destination_floor] = 1

    def adjust_acceleration(self, acceleration):
        self.acceleration = acceleration

    def adjust_speed(self, simulation_step):
        # change speed with second, the speed can't beyond max_speed
        self.cur_speed += self.acceleration * simulation_step
        if abs(self.cur_speed) > abs(self.max_speed):
            self.cur_speed = self.max_speed * abs(self.cur_speed)/self.cur_speed
        if abs(self.cur_speed) < 1e-2:
            self.cur_speed = 0
        print("speed:", self.cur_speed)

    def adjust_height(self, simulation_step):
        self.current_height = self.current_height +\
                              self.cur_speed * simulation_step + self.acceleration/2*simulation_step**2
        # consider elevator reaches the floor if the absolute error equals to 0.01
        if abs(self.current_height-round(self.current_height)) < 1e-2:
            self.current_height = round(self.current_height)

