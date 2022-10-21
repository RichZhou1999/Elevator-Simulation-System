import numpy as np
from Passenger import Passenger
from Controller import Controller
import uuid


class System:
    def __init__(self, system_para):
        self.arrival_rate_up = system_para["arrival_rate_up"]
        self.arrival_rate_down = system_para["arrival_rate_down"]
        self.simulation_time = system_para["simulation_time"]
        self.simulation_step = system_para["simulation_step"]
        self.building = system_para["building"]
        self.controller = Controller()
        self.elevators = {}
        self.wait_passengers = []
        self.run_passengers = []
        self.past_passengers = []
        self.request_signal_list_up = []
        self.request_signal_list_down = []
        self.elevator_max_wait_time = system_para["elevator_max_wait_time"]

    def reset(self):
        height_floor_dict = self.building.height_floor_dict
        floor_num = len(height_floor_dict.values())
        for elevator in self.elevators:
            elevator.request_floor_list = [0] * floor_num
        self.request_signal_list_down = [0] * floor_num
        self.request_signal_list_up = [0] * floor_num



    def add_elevator(self, elevator, name):
        if name not in self.elevators:
            self.elevators[name] = elevator
        else:
            raise Exception("name already exist")

    def run(self):
        self.reset()
        for i in range(self.simulation_time):
            self.passenger_generator_up()
            self.passenger_generator_down()
            self.adjust_passenger_state()
            self.adjust_elevator_state()
            self.simulation_time += 1

    def check_elevator_wait_state(self, elevator):
        if elevator.state == "wait":
            if elevator.cur_waited_time < self.elevator_max_wait_time:
                elevator.cur_waited_time += 1
                return True
            else:
                elevator.state == "run"
                return False

    def adjust_elevator_state(self):
        accelerations = Controller.get_acceleration(self)
        for i in range(len(self.elevators)):
            elevator = self.elevators[i]
            if self.check_elevator_wait_state(elevator):
                continue
            elevator.update(self.simulation_step, accelerations[i])
            if abs(elevator.current_height - self.building.floor_height_dict[elevator.destination_floor]):
                elevator.set_state("wait")
                elevator.cur_waited_time = 0

    def adjust_passenger_state(self):
        for elevator in self.elevators:
            if elevator.state == "wait":
                # passengers come out when get to the destination
                if elevator.cur_waited_time == 0:
                    self.adjust_request_signal(self.building.height_floor_dict[elevator.current_height],
                                               elevator.direction,
                                               signal_type="minus")
                    get_out_passengers = []
                    for i in range(len(elevator.current_passenger_list)):
                        passenger = elevator.current_passenger_list[i]
                        if passenger.destination_floor == self.building.height_floor_dict[elevator.current_height] and \
                                passenger.state == "run":
                            del elevator.current_passenger_list[i]
                            get_out_passengers.append(passenger)
                            elevator.current_accommodation -= 1
                    self.past_passengers += get_out_passengers
                else:
                    # new passengers come in
                    get_in_passengers = []
                    for i in range(len(self.wait_passengers)):
                        passenger = self.wait_passengers[i]
                        if passenger.starting_floor == self.building.height_floor_dict[elevator.current_height] and \
                                passenger.state == "wait" and elevator.current_accommodation < elevator.capacity:
                            passenger.state = "run"
                            get_in_passengers.append(passenger)
                            elevator.current_accommodation += 1
                            del self.wait_passengers[i]
                    elevator.current_passenger_list = elevator.current_passenger_list + get_in_passengers

    def passenger_generator_up(self):
        passengers = []
        max_floor = self.building.max_floor
        number = np.random.poisson(self.arrival_rate_up)
        for i in range(number):
            destination_floor = np.random.randint(1, max_floor+1)
            temp_p = Passenger(uuid.uuid4(), 0, destination_floor)
            self.adjust_request_signal(destination_floor, "up", signal_type="add")
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
        self.adjust_request_signal(0, "down", signal_type="add")
        self.wait_passengers += passengers

    def adjust_request_signal(self, floor, direction, signal_type="add"):
        if direction == "up":
            if signal_type == "add":
                self.request_signal_list_up[floor] = 1
            elif signal_type == "minus":
                self.request_signal_list_up[floor] = 0
        elif direction == "down":
            if signal_type == "add":
                self.request_signal_list_down[floor] = 1
            elif signal_type == "minus":
                self.request_signal_list_down[floor] = 0


