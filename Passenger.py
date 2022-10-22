import numpy as np
import uuid
import copy
'''
@attribute:
    pid: passenger id (string)
    starting_floor: the floor where the passenger start(int)
    destination_floor: the floor where the passenger ends(int)
    state: "wait"(wait for the elevator to come) or "run"( on the elevator) or "finished" 
'''


class Passenger:
    def __init__(self, pid, starting_floor, destination_floor):
        self.pid = pid
        self.starting_floor = starting_floor
        self.destination_floor = destination_floor
        self.state = "wait"