from Building.Building import Building
from Elevator.Elevator import Elevator
from System.System import System
from Controller.Controller import Controller_one_elevator
from Controller.ControllerByTheWay import ControllerByTheWay
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

system_para = {"arrival_rate_up": 0.1,
               "arrival_rate_down": 0.1,
               "building": building,
               "simulation_time": 1000,
               "simulation_step": 1,
               "elevator_max_wait_time": 10,
               "controller": ControllerByTheWay,
               "safety_deceleration_distance": 1,
               "show_process_output": False
               }

system = System(system_para)
system.add_elevator(elevator)
system.run()

