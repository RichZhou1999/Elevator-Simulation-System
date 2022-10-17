from Building import Building
from Elevator import Elevator
from System import System
from Controller import Controller
'''
Construct the system gradually with building, elevator, controller
'''

height_floor_dict = {0: 0,
                     3: 1,
                     6: 2}

building = Building(height_floor_dict)

elevator = Elevator(capacity=16, max_speed=10, controller=Controller)

system_para = {"arrival_rate_up": 10,
               "arrival_rate_down": 10,
               "building": building,
               "simulation_time": 1000}

system = System(system_para)
system.add_elevator(elevator, "elevator1")
system.add_elevator(elevator, "elevator2")
system.run()

