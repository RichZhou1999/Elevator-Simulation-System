import numpy as np
from Building.Building import Building
from Elevator.Elevator import Elevator
from System.System_passener_no_stop_low_level import System
# from Controller.Controller import Controller_one_elevator
from Controller.ControllerMultipleElevators import ControllerMultipleElevators

'''
Construct the system gradually with building, elevator, controller
direction: up is positive and down is negative applying to acceleration, 
speed and height
'''

# height_floor_dict = {0: 0,
#                      3: 1,
#                      6: 2,
#                      9: 3,
#                      12: 4,
#                      15: 5}
# feasible_floor = [1, 1, 1, 1, 1, 1]
height_floor_dict = {}
total_floor = 5
for i in range(total_floor+1):
    height_floor_dict[3*i] = i
feasible_floor = [1]*(total_floor+1)
building = Building(height_floor_dict)

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

elevator3 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator3",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

elevator4 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator4",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

elevator5 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator5",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

elevator6 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator6",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

elevator7 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator7",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

elevator8 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator8",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

elevator9 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator9",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

elevator10 = Elevator(capacity=16,
                    max_speed=2,
                    name="elevator10",
                    max_acceleration=0.5,
                    feasible_floor=feasible_floor)

system_para = {"arrival_rate_up": 0.1,
               "arrival_rate_down": 0.1,
               "building": building,
               "simulation_time": 10000,
               "simulation_step": 1,
               "elevator_max_wait_time": 10,
               "controller": ControllerMultipleElevators,
               "safety_deceleration_distance": 1,
               "show_process_output": False}

system = System(system_para)
system.add_elevator(elevator)
system.add_elevator(elevator2)
system.add_elevator(elevator3)
system.add_elevator(elevator4)
# system.add_elevator(elevator5)
# system.add_elevator(elevator6)
# system.add_elevator(elevator7)
# system.add_elevator(elevator8)
# system.add_elevator(elevator9)
# system.add_elevator(elevator10)


result = []
for i in range(10):
    result.append(system.run())
print("wait time list ", result)
print("mean of wait time: ", np.mean(result))
print("standard deviation of wait time: ", np.std(result))

