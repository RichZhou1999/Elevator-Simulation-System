from Building import Building
from Elevator import Elevator
from System import System
from Controller import Controller, Controller_one_elevator
'''
Construct the system gradually with building, elevator, controller
direction: up is positive and down is negative applying to acceleration, 
speed and height
'''

height_floor_dict = {0: 0,
                     3: 1,
                     6: 2,
                     9: 3,
                     12: 4,
                     15: 5}

building = Building(height_floor_dict)

elevator = Elevator(capacity=16,
                    max_speed=10,
                    name="elevator1",
                    acceleration=0.5)

system_para = {"arrival_rate_up": 3,
               "arrival_rate_down": 3,
               "building": building,
               "simulation_time": 1000,
               "simulation_step": 1,
               "elevator_max_wait_time": 30,
               "controller": Controller_one_elevator,
               "safety_deceleration_distance": 1}

system = System(system_para)
system.add_elevator(elevator)
system.run()

