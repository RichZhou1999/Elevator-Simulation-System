import numpy as np
from Passenger import Passenger
from Controller import Controller, Controller_one_elevator
import uuid


class System:
    def __init__(self, system_para):
        self.arrival_rate_up = system_para["arrival_rate_up"]
        self.arrival_rate_down = system_para["arrival_rate_down"]
        self.simulation_time = system_para["simulation_time"]
        self.simulation_step = system_para["simulation_step"]
        self.elevator_max_wait_time = system_para["elevator_max_wait_time"]
        self.building = system_para["building"]
        self.controller = system_para["controller"]()
        self.elevators = []
        self.elevator_name_list = []
        self.wait_passengers = []
        self.run_passengers = []
        self.past_passengers = []
        self.request_signal_list_up = []
        self.request_signal_list_down = []
        self.current_simulation_time = 0
        self.elevator_max_wait_time = system_para["elevator_max_wait_time"]
        self.elevator_safety_deceleration_distance = system_para["safety_deceleration_distance"]


    def reset(self):
        height_floor_dict = self.building.height_floor_dict
        floor_num = len(height_floor_dict.values())
        for elevator in self.elevators:
            elevator.request_floor_list = [0] * floor_num
        self.request_signal_list_down = [0] * floor_num
        self.request_signal_list_up = [0] * floor_num
        self.wait_passengers = []
        self.run_passengers = []
        self.past_passengers = []

    def add_elevator(self, elevator):
        if elevator.name not in self.elevator_name_list:
            self.elevator_name_list.append(elevator.name)
            self.elevators.append(elevator)
        else:
            raise Exception("name already exist")

    def run(self):
        self.reset()
        for i in range(self.simulation_time):
            self.passenger_generator_up()
            self.passenger_generator_down()
            self.adjust_passenger_state()
            self.adjust_elevator_state()
            self.current_simulation_time += 1
            print("state:", self.elevators[0].state)
            print("direction:", self.elevators[0].direction)
            print( "time: ", self.current_simulation_time)
            print("elevator_request_list: ", self.elevators[0].request_floor_list)
            print("request_signal_list_up:", self.request_signal_list_up)
            print("request_signal_list_down:", self.request_signal_list_down)
            passenger_des = []
            for passenger in self.elevators[0].current_passenger_list:
                print("des_p:", passenger.destination_floor )
                passenger_des.append(passenger.destination_floor)
            print(passenger_des)
            print("-"*30)

    def check_elevator_wait_state(self, elevator):
        if elevator.state == "wait":
            if elevator.cur_waited_time < self.elevator_max_wait_time:
                elevator.cur_waited_time += 1
                return True
            else:
                elevator.set_state("run")
                return False

    def adjust_elevator_state(self):
        for i in range(len(self.elevators)):
            elevator = self.elevators[i]
            elevator.adjust_height(self.simulation_step)
            elevator.adjust_speed(self.simulation_step)
            elevator.adjust_request_floor_list()
            # print("11", elevator.destination_floor)
            # print(elevator.current_height)
            if elevator.destination_floor != None and elevator.current_height - self.building.floor_height_dict[elevator.destination_floor] == 0 and \
                    elevator.state != "wait":
                cur_floor = self.building.height_floor_dict[elevator.current_height]
                print("-"*30)
                print("cur_floor: ", cur_floor)
                print("_"*30)
                self.adjust_request_signal(cur_floor, elevator.state, signal_type="minus")
                elevator.request_floor_list[cur_floor] = 0
                elevator.set_state("wait")
                elevator.adjust_acceleration(acceleration=0)
                elevator.cur_waited_time = 0
                elevator.current_height = self.building.floor_height_dict[elevator.destination_floor]
                continue
            if self.check_elevator_wait_state(elevator):
                continue
            # elevator.adjust_height(self.simulation_step)
            # elevator.adjust_speed(self.simulation_step)
            # elevator.adjust_request_floor_list()
        accelerations = self.controller.get_acceleration(self)
        for i in range(len(self.elevators)):
            elevator = self.elevators[i]
            if elevator.state == "wait":
                continue
            elevator.adjust_acceleration(acceleration=accelerations[i])
            print("height: ", elevator.current_height)

    def adjust_passenger_state(self):
        for elevator in self.elevators:
            if elevator.state == "wait":
                # passengers come out when get to the destination
                if elevator.cur_waited_time == 0:
                    self.adjust_request_signal(self.building.height_floor_dict[elevator.current_height],
                                               elevator.direction,
                                               signal_type="minus")
                    elevator.request_floor_list[self.building.height_floor_dict[elevator.current_height]]=0
                    print("coming out" + "!"*10)
                    get_out_passengers = []
                    temp_cur_passengers = []
                    for i in range(len(elevator.current_passenger_list)):
                        passenger = elevator.current_passenger_list[i]
                        if passenger.destination_floor == self.building.height_floor_dict[elevator.current_height] and \
                                passenger.state == "run":
                            get_out_passengers.append(passenger)
                            elevator.current_accommodation -= 1
                        else:
                            temp_cur_passengers.append(passenger)
                    self.past_passengers += get_out_passengers
                    elevator.current_passenger_list = temp_cur_passengers
                else:
                    # new passengers come in
                    get_in_passengers = []
                    temp_wait_passengers = []
                    for i in range(len(self.wait_passengers)):
                        passenger = self.wait_passengers[i]
                        if passenger.starting_floor == self.building.height_floor_dict[elevator.current_height] and \
                                passenger.state == "wait" and elevator.current_accommodation < elevator.capacity:
                            passenger.state = "run"
                            get_in_passengers.append(passenger)
                            elevator.current_accommodation += 1
                        else:
                            temp_wait_passengers.append(passenger)
                    elevator.current_passenger_list = elevator.current_passenger_list + get_in_passengers
                    self.wait_passengers = temp_wait_passengers

    def passenger_generator_up(self):
        passengers = []
        max_floor = len(self.building.height_floor_dict.keys()) - 1
        number = np.random.poisson(self.arrival_rate_up)
        for i in range(number):
            destination_floor = np.random.randint(1, max_floor+1)
            temp_p = Passenger(uuid.uuid4(), starting_floor=0, destination_floor=destination_floor)
            self.adjust_request_signal(0, "up", signal_type="add")
            passengers.append(temp_p)
        self.wait_passengers += passengers

    def passenger_generator_down(self):
        passengers = []
        max_floor = len(self.building.height_floor_dict.keys()) - 1
        single_floor_arrival_rate = self.arrival_rate_down / (max_floor - 1)
        for i in range(1, max_floor + 1):
            number = np.random.poisson(single_floor_arrival_rate)
            for j in range(number):
                temp_p = Passenger(uuid.uuid4(), starting_floor=i, destination_floor=0)
                passengers.append(temp_p)
                self.adjust_request_signal(i, "down", signal_type="add")
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


