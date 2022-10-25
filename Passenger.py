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
    def __init__(self, pid, starting_floor, destination_floor, start_time):
        self.pid = pid
        self.starting_floor = starting_floor
        self.destination_floor = destination_floor
        self.state = "wait"
        self._start_time = start_time
        self._get_on_elevator_time = 0
        self._arrival_time = 0

    @property
    def start_time(self):
        return self._start_time

    @property
    def get_on_elevator_time(self):
        return self._get_on_elevator_time

    @property
    def arrival_time(self):
        return self._arrival_time

    def set_get_on_elevator_time(self, time):
        self._get_on_elevator_time = time

    def set_arrival_time(self, time):
        self._arrival_time = time

    def __repr__(self):
        print("start_time:", self.start_time)
        print("get_on_elevator_time:", self.get_on_elevator_time)
        print("wait_time", self.get_on_elevator_time, self.start_time)

if __name__ == "__main__":
    test_p = Passenger(uuid.uuid4(),
                       starting_floor=0,
                       destination_floor=10,
                       start_time=10)
    test_p.set_get_on_elevator_time(100)
    test_p.set_arrival_time(200)
    print(test_p)