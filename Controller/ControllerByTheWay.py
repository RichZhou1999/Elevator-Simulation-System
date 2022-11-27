from Controller.Controller import Controller, Controller_one_elevator


class ControllerByTheWay(Controller_one_elevator):
    @staticmethod
    def get_highest_elevator(system):
        highest_elevator = system.elevators[0]
        for elevator in system.elevators:

            if elevator.current_height > highest_elevator.current_height:
                highest_elevator = elevator
            elif elevator.current_height == highest_elevator.current_height:
                if elevator.state == "wait" and highest_elevator.state == "wait":
                    if elevator.cur_waited_time > highest_elevator.cur_waited_time:
                        highest_elevator = elevator
                elif elevator.state != "wait" and highest_elevator.state == "wait":
                    highest_elevator = elevator
        # system.highest_elevator = highest_elevator
        return highest_elevator

    def get_upper_destination(self, system, elevator,
                              request_signal_list_up,
                              request_signal_list_down,
                              cur_floor,
                              elevator_request_signal_list):
        feasible_floor = elevator.feasible_floor
        temp = []
        for i in range(len(feasible_floor)):
            if feasible_floor[i] == 1 and request_signal_list_down[i] == 1:
                temp.append(1)
            else:
                temp.append(0)
        request_signal_list_down = temp
        request_down = request_signal_list_down[cur_floor + 1:]
        elevator_request_signal_list_upper = elevator_request_signal_list[cur_floor + 1:]
        if elevator_request_signal_list_upper.count(1):
            return elevator_request_signal_list_upper.index(1) + cur_floor + 1
        # waiting passengers want to go lower from upper part, so calculate the highest floor with request
        # elif request_down.count(1) and self.get_highest_elevator(system) == elevator:
        elif request_down.count(1) and self.get_highest_elevator(system) == elevator:
            # if system.highest_elevator == elevator:
            # and system.highest_elevator == None and self.get_highest_elevator(system) == elevator:
            # self.get_highest_elevator(system) == elevator:
            max_index = 0
            for i in range(len(request_down)):
                if request_down[i] == 1:
                    max_index = i
            return max_index + cur_floor + 1
        # no need to go upper
        else:
            if elevator.current_height != 0:
                # if elevator == system.highest_elevator:
                #     system.highest_elevator = None
                elevator.set_direction("down")
                print("elevator direction switch to down")
                return self.get_lower_destination(system, elevator, request_signal_list_up, request_signal_list_down,
                                                  cur_floor,
                                                  elevator_request_signal_list)
            else:
                return 0

    def get_lower_destination(self, system, elevator, request_signal_list_up,
                              request_signal_list_down,
                              cur_floor,
                              elevator_request_signal_list):
        feasible_floor = elevator.feasible_floor
        temp = []
        for i in range(len(feasible_floor)):
            if feasible_floor[i] == 1 and request_signal_list_down[i] == 1:
                temp.append(1)
            else:
                temp.append(0)
        request_signal_list_down = temp
        request_down = request_signal_list_down[0: cur_floor + 1]
        elevator_request_signal_list_lower = elevator_request_signal_list[0: cur_floor + 1]
        # invert request_down, elevator_request_signal_list_lower from higher to lower
        temp1 = request_down[::-1]
        temp2 = elevator_request_signal_list_lower[::-1]
        if request_down.count(1) and elevator_request_signal_list_lower.count(1):
            return cur_floor - min(temp1.index(1), temp2.index(1))
        # only passengers in the elevator want to go lower
        elif elevator_request_signal_list_lower.count(1):
            return cur_floor - temp2.index(1)
        # only waiting passengers request go lower
        elif request_down.count(1):
            return cur_floor - temp1.index(1)
        # no inner and outer request to go lower
        else:
            if cur_floor == 0 and elevator.current_height == 0:
                elevator.set_direction("up")
                print("elevator direction switch to up")
                return self.get_upper_destination(system, elevator, request_signal_list_up, request_signal_list_down, cur_floor,
                                             elevator_request_signal_list)
            else:
                return 0