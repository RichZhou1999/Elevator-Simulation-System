import numpy as np
from Passenger import Passenger
import uuid


class System:
    def __init__(self, system_para):
        self.arrival_rate_up = system_para["arrival_rate_up"]
        self.arrival_rate_down = system_para["arrival_rate_down"]
        self.simulation_time = system_para["simulation_time"]
        self.building = system_para["building"]
        self.elevators = {}
        self.wait_passengers = []
        self.run_passengers = []
        self.past_passengers = []

    def add_elevator(self, elevator, name):
        if name not in self.elevators:
            self.elevators[name] = elevator
        else:
            raise Exception("name already exist")

    def run(self):
        for i in range(self.simulation_time):
            self.passenger_generator_up()
            self.passenger_generator_down()
            self.adjust_elevator_state()
            self.adjust_passenger_state()


    def adjust_elevator_state(self):
        for elevator in self.elevators:
            elevator.update(self)


    def adjust_passenger_state(self):
        for elevator in self.elevators:
            if elevator.state == "wait":
                # passengers come out when get to the destination
                if elevator.cur_waited_time == 0:
                    get_out_passengers = []
                    for i in range(len(self.run_passengers)):
                        passenger = self.run_passengers[i]
                        if passenger.destination_floor == self.building.height_floor_dict[elevator.current_height] and \
                                passenger.state == "run":
                            del self.run_passengers[i]
                            get_out_passengers.append(passenger)
                    self.past_passengers += get_out_passengers
                    pass
                else:
                    # new passengers come in
                    get_in_passengers = []
                    for i in range(len(self.wait_passengers)):
                        passenger = self.wait_passengers[i]
                        if passenger.starting_floor == self.building.height_floor_dict[elevator.current_height] and \
                                passenger.state == "wait":
                            passenger.state = "run"
                            get_in_passengers.append(passenger)
                    self.run_passengers = self.run_passengers + get_in_passengers


    def passenger_generator_up(self):
        passengers = []
        max_floor = self.building.max_floor
        number = np.random.poisson(self.arrival_rate_up)
        for i in range(number):
            destination_floor = np.random.randint(1, max_floor+1)
            temp_p = Passenger(uuid.uuid4(), 0, destination_floor)
            passengers.append(temp_p)
        self.wait_passengers += passengers

    def passenger_generator_down(self):
        passengers = []
        max_floor = self.building.max_floor
        single_floor_arrival_rate = self.arrival_rate_down / (max_floor - 1)
        for i in range(1, max_floor):
            number = np.random.poisson(single_floor_arrival_rate)
            for j in range(number):
                temp_p = Passenger(uuid.uuid4(), i, 0)
                passengers.append(temp_p)
        self.wait_passengers += passengers

