import numpy as np
from Building.Building import Building
from Elevator.Elevator import Elevator
from System.System import System
from Controller.Controller import Controller_one_elevator
from Controller.ControllerMultipleElevators import ControllerMultipleElevators
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

feasible_floor = [1, 1, 1, 1, 1, 1]
elevator = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator1",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

elevator2 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator2",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

# elevator3 = Elevator(capacity=16,
#                     max_speed=2,
#                     name="elevator3",
#                     max_acceleration=0.5,
#                     feasible_floor=feasible_floor)

system_para = {"arrival_rate_up": 0.1,
               "arrival_rate_down": 0.1,
               "building": building,
               "simulation_time": 10000,
               "simulation_step": 1,
               "elevator_max_wait_time": 2,
               "controller": ControllerMultipleElevators,
               "safety_deceleration_distance": 1,
               "show_process_output": True
               }

system = System(system_para)
system.add_elevator(elevator)
system.add_elevator(elevator2)
# system.add_elevator(elevator3)
for i in range(1):
    system.run()

