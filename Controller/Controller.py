from abc import ABCMeta, abstractmethod
import bisect

'''

'''


def calculate_min_deceleration_distance(cur_speed, max_acceleration, max_deceleration_time=20):
    # formula: v^2 = 2ax
    min_deceleration_distance = 0
    for i in range(1, max_deceleration_time + 1):
        if cur_speed == 0:
            break
        if abs(cur_speed / i) <= abs(max_acceleration):
            a = cur_speed / i
            min_deceleration_distance = abs(cur_speed ** 2 / 2 / a)
            break
    return min_deceleration_distance


from abc import ABCMeta, abstractmethod
import bisect


class Controller:
    def __init__(self):
        pass

    '''
    Regard that the parameter:system contains all the information including all passengers, elevators
    building.
    '''

    # these two abstract method will be implemented in different controller(control 1/2/3... elevators)
    @abstractmethod
    def get_acceleration(self, system):
        pass

    @abstractmethod
    def get_destination_floor(self, system):
        pass

    # will be called in class Controler_one_elevator.get_acceleration
    @staticmethod
    def calculate_acceleration(cur_height,
                               destination_height,
                               cur_speed,
                               max_acceleration,
                               max_speed,
                               safety_deceleration_distance=1,
                               max_deceleration_time=20):
        acceleraion = 0

        delta_height = destination_height - cur_height
        min_deceleration_distance = calculate_min_deceleration_distance(cur_speed,
                                                                        max_acceleration) \
                                    + safety_deceleration_distance + abs(cur_speed)
        print("delta:", delta_height)
        # special condition: arrived
        if delta_height == 0:
            return 0
        # special condition: elevator is initially static and has enough distance to deaccelerate
        if cur_speed == 0:
            if abs(delta_height) > min_deceleration_distance:
                return max_acceleration * abs(delta_height) / delta_height
        # has enough distance to deaccelerate
        if abs(delta_height) > min_deceleration_distance:
            # max accelerate
            if abs(cur_speed) < max_speed:
                acceleraion = max_acceleration * abs(delta_height) / delta_height
            # uniform speed
            elif abs(cur_speed) == max_speed:
                acceleraion = 0
        # need to deaccelerate, the direction of acceleration depends on the direction of speed
        elif abs(delta_height) <= min_deceleration_distance:
            for i in range(1, max_deceleration_time + 1):
                if abs(cur_speed / i) < abs(max_acceleration):
                    if cur_speed > 0:
                        acceleraion = -cur_speed ** 2 / 2 / delta_height * cur_speed / abs(cur_speed)
                    elif cur_speed < 0:
                        acceleraion = -cur_speed ** 2 / 2 / delta_height
                    break
        return round(acceleraion, 4)


"add new controllers and algorithms here"


class Controller_one_elevator(Controller):
    # will be called in function get_acceleration
    # SCAN algorithm

    def get_upper_destination(self, system, elevator, request_signal_list_up,
                              request_signal_list_down,
                              cur_floor,
                              elevator_request_signal_list):
        request_down = request_signal_list_down[cur_floor + 1:]
        elevator_request_signal_list_upper = elevator_request_signal_list[cur_floor + 1:]
        # running passengers want to go upper floor
        if elevator_request_signal_list_upper.count(1):
            return elevator_request_signal_list_upper.index(1) + cur_floor + 1
        # waiting passengers want to go lower from upper part, so calculate the highest floor with request
        elif request_down.count(1):
            max_index = 0
            for i in range(len(request_down)):
                if request_down[i] == 1:
                    max_index = i
            return max_index + cur_floor + 1
        # no need to go upper
        else:
            if elevator.current_height != 0:
                elevator.set_direction("down")
                print("elevator direction switch to down")
                return self.get_lower_destination(system, elevator, request_signal_list_up, request_signal_list_down, cur_floor,
                                             elevator_request_signal_list)
            else:
                return 0

    def get_lower_destination(self, system, elevator, request_signal_list_up,
                              request_signal_list_down,
                              cur_floor,
                              elevator_request_signal_list):
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

    def get_destination_floor(self, system, elevator, ):
        # properties from system and elevator
        cur_height = elevator.current_height
        request_signal_list_up = system.request_signal_list_up
        request_signal_list_down = system.request_signal_list_down
        elevator_request_signal_list = elevator.request_floor_list
        cur_speed = elevator.cur_speed
        max_acceleration = elevator.max_acceleration
        # this list contains height
        floor_height_list = list(system.building.height_floor_dict.keys())
        cur_floor = bisect.bisect_right(floor_height_list, cur_height) - 1
        min_deceleration_distance = calculate_min_deceleration_distance(cur_speed, max_acceleration)
        # renew the cur_floor to make it more accurate
        if cur_floor + 1 < len(floor_height_list) and elevator.direction == "up":
            if abs(cur_height - system.building.floor_height_dict[cur_floor + 1]) - min_deceleration_distance < -1e-2:
                cur_floor += 1
        if cur_floor - 1 >= 0 and cur_floor + 1 < len(floor_height_list) and elevator.direction == "down":
            if abs(cur_height - system.building.floor_height_dict[cur_floor - 1]) - min_deceleration_distance < -1e-2:
                cur_floor -= 1
        elevator.cur_floor = cur_floor
        # print("%s cur_floor:" % elevator.name, cur_floor)

        # def get_upper_destination(elevator, request_signal_list_up,
        #                           request_signal_list_down,
        #                           cur_floor,
        #                           elevator_request_signal_list):
        #     request_down = request_signal_list_down[cur_floor + 1:]
        #     elevator_request_signal_list_upper = elevator_request_signal_list[cur_floor + 1:]
        #     # running passengers want to go upper floor
        #     if elevator_request_signal_list_upper.count(1):
        #         return elevator_request_signal_list_upper.index(1) + cur_floor + 1
        #     # waiting passengers want to go lower from upper part, so calculate the highest floor with request
        #     elif request_down.count(1):
        #         max_index = 0
        #         for i in range(len(request_down)):
        #             if request_down[i] == 1:
        #                 max_index = i
        #         return max_index + cur_floor + 1
        #     # no need to go upper
        #     else:
        #         if elevator.current_height != 0:
        #             elevator.set_direction("down")
        #             print("elevator direction switch to down")
        #             return get_lower_destination(request_signal_list_up, request_signal_list_down, cur_floor,
        #                                          elevator_request_signal_list)
        #         else:
        #             return 0
        #
        # def get_lower_destination(request_signal_list_up,
        #                           request_signal_list_down,
        #                           cur_floor,
        #                           elevator_request_signal_list):
        #     request_down = request_signal_list_down[0: cur_floor + 1]
        #     elevator_request_signal_list_lower = elevator_request_signal_list[0: cur_floor + 1]
        #     # invert request_down, elevator_request_signal_list_lower from higher to lower
        #     temp1 = request_down[::-1]
        #     temp2 = elevator_request_signal_list_lower[::-1]
        #     if request_down.count(1) and elevator_request_signal_list_lower.count(1):
        #         return cur_floor - min(temp1.index(1), temp2.index(1))
        #     # only passengers in the elevator want to go lower
        #     elif elevator_request_signal_list_lower.count(1):
        #         return cur_floor - temp2.index(1)
        #     # only waiting passengers request go lower
        #     elif request_down.count(1):
        #         return cur_floor - temp1.index(1)
        #     # no inner and outer request to go lower
        #     else:
        #         if cur_floor == 0 and elevator.current_height == 0:
        #             elevator.set_direction("up")
        #             print("elevator direction switch to up")
        #             return get_upper_destination(request_signal_list_up, request_signal_list_down, cur_floor,
        #                                          elevator_request_signal_list)
        #         else:
        #             return 0

        if elevator.direction == "up" or elevator.direction == None:
            destination_floor = self.get_upper_destination(system, elevator,
                                                           request_signal_list_up,
                                                           request_signal_list_down,
                                                           cur_floor,
                                                           elevator_request_signal_list)
        elif elevator.direction == "down":
            destination_floor = self.get_lower_destination(system, elevator, request_signal_list_up,
                                                           request_signal_list_down,
                                                           cur_floor,
                                                           elevator_request_signal_list)
        # print("%s: destination_floor: " % elevator.name, destination_floor)
        return destination_floor

    def get_acceleration(self, system):
        height_floor_dict = system.building.height_floor_dict
        safety_deceleration_distance = system.elevator_safety_deceleration_distance
        accelerations = []
        for i in range(len(system.elevators)):
            elevator = system.elevators[i]
            cur_height = elevator.current_height
            cur_speed = elevator.cur_speed
            # find next destination floor
            destination_floor = self.get_destination_floor(system, elevator)
            elevator.destination_floor = destination_floor
            destination_height = system.building.floor_height_dict[destination_floor]
            max_acceleration = elevator.max_acceleration
            max_speed = elevator.max_speed
            # calculate the acceleration at certain timestep, result will be returned in System.adjust_elevator_state
            acceleration = self.calculate_acceleration(cur_height,
                                                       destination_height,
                                                       cur_speed,
                                                       max_acceleration,
                                                       max_speed,
                                                       safety_deceleration_distance
                                                       )
            accelerations.append(acceleration)
        print("accelerations: ", accelerations)
        return accelerations
