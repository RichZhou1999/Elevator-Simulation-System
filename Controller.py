from abc import ABCMeta, abstractmethod
import bisect

'''

'''


def calculate_min_deceleration_distance(cur_speed, max_acceleration, max_deceleration_time=20):
    min_deceleration_distance = 0
    for i in range(1, max_deceleration_time+1):
        if cur_speed == 0:
            break
        if abs(cur_speed/i) <= abs(max_acceleration):
            a = cur_speed/i
            min_deceleration_distance = abs(cur_speed**2/2/a)
            break
    return min_deceleration_distance


class Controller:
    def __init__(self):
        pass

    '''
    Regard that the parameter:system contains all the information including all passengers, elevators
    building.
    '''
    @abstractmethod
    def get_acceleration(self, system):
        pass

    @abstractmethod
    def get_destination_floor(self, system):
        pass
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
                                                                        max_acceleration) + safety_deceleration_distance
        print("delta:", delta_height)
        if delta_height == 0:
            return 0
        if cur_speed == 0:
            if delta_height > min_deceleration_distance:
                return max_acceleration * abs(delta_height) / delta_height
        if abs(delta_height) > min_deceleration_distance:
            if abs(cur_speed) < max_speed:
                acceleraion = max_acceleration * abs(delta_height) / delta_height
            elif abs(cur_speed) == max_speed:
                acceleraion = 0
        elif abs(delta_height) <= min_deceleration_distance:
            for i in range(1, max_deceleration_time + 1):
                if abs(cur_speed / i) < abs(max_acceleration):
                    acceleraion = -cur_speed ** 2 / 2 / delta_height * cur_speed / abs(cur_speed)
                    break
        return acceleraion


"add new controllers and algorithms here"

class Controller_one_elevator(Controller):
    def get_destination_floor(self, system, elevator, ):
        cur_height = elevator.current_height
        request_signal_list_up = system.request_signal_list_up
        request_signal_list_down = system.request_signal_list_down
        elevator_request_signal_list = elevator.request_floor_list
        cur_speed = elevator.cur_speed
        max_acceleration = elevator.max_acceleration
        floor_height_list = list(system.building.height_floor_dict.keys())
        cur_floor = bisect.bisect_right(floor_height_list, cur_height) - 1
        min_deceleration_distance = calculate_min_deceleration_distance(cur_speed, max_acceleration)
        cur_height = elevator.current_height
        if cur_floor + 1 < len(floor_height_list) and elevator.direction == "up":
            if abs(cur_height - system.building.floor_height_dict[cur_floor + 1]) < min_deceleration_distance:
                cur_floor += 1
        if cur_floor - 1 >= 0 and elevator.direction == "down":
            if abs(cur_height - system.building.floor_height_dict[cur_floor + 1]) < min_deceleration_distance:
                cur_floor -= 1
        print("cur_floor:", cur_floor)

        def get_upper_destination(request_signal_list_up,
                                  request_signal_list_down,
                                  cur_floor,
                                  elevator_request_signal_list):
            request_upper = request_signal_list_up[cur_floor + 1:]
            elevator_request_signal_list_upper = elevator_request_signal_list[cur_floor + 1:]
            if request_upper.count(1) and elevator_request_signal_list_upper.count(1):
                return min(request_upper.index(1), elevator_request_signal_list_upper.index(1)) + cur_floor + 1
            elif (not elevator_request_signal_list_upper.count(1)) and (not request_upper.count(1)):
                elevator.set_direction("Down")
                print("elevator direction switch to down")
                return get_lower_destination(request_signal_list_up, request_signal_list_down, cur_floor,
                                             elevator_request_signal_list)
            elif not elevator_request_signal_list_upper.count(1):
                return request_upper.index(1) + cur_floor + 1
            elif not request_upper.count(1):
                return elevator_request_signal_list_upper.index(1) + cur_floor + 1
        def get_lower_destination(request_signal_list_up,
                                  request_signal_list_down,
                                  cur_floor,
                                  elevator_request_signal_list):
            request_lower = request_signal_list_down[0: cur_floor + 1]
            elevator_request_signal_list_lower = elevator_request_signal_list[0: cur_floor + 1]
            temp1 = request_lower[::-1]
            temp2 = elevator_request_signal_list_lower[::-1]
            if request_lower.count(1) and elevator_request_signal_list_lower.count(1):
                return cur_floor - min(temp1.index(1), temp2.index(1))
            elif (not request_lower.count(1)) and (not elevator_request_signal_list_lower.count(1)):
                return 0
            elif not request_lower.count(1):
                return cur_floor - temp2.index(1)
            elif not elevator_request_signal_list_lower.count(1):
                return cur_floor - temp1.index(1)

        if elevator.direction == "up" or elevator.direction == None:
            destination_floor = get_upper_destination(request_signal_list_up,
                                                      request_signal_list_down,
                                                      cur_floor,
                                                      elevator_request_signal_list)
        elif elevator.direction == "down":
            destination_floor = get_lower_destination(request_signal_list_up,
                                                      request_signal_list_down,
                                                      cur_floor,
                                                      elevator_request_signal_list)
        print("destination_floor: ", destination_floor)
        return destination_floor

    # def get_destination_floor(self, system, elevator):
    #     request_signal_list_up = system.request_signal_list_up
    #     request_signal_list_down = system.request_signal_list_down
    #     elevator_request_signal_list = elevator.request_floor_list
    #     cur_height = elevator.current_height
    #     floor_height_list = list(system.building.height_floor_dict.keys())
    #     cur_floor = bisect.bisect_right(floor_height_list, cur_height) - 1
    #     print("cur_floor:", cur_floor)
    #     def check_has_signal(*args, **kwargs):
    #         def inner(f):
    #             def inner2(*args, **kwargs):
    #                 return f(*args, **kwargs)
    #             return inner2
    #         def zero(f):
    #             def innerzero(f):
    #                 return 0
    #             return innerzero
    #         if request_signal_list_up.count(1) == 0 and request_signal_list_down == 0:
    #             return zero
    #         else:
    #             return inner
    #
    #     @check_has_signal(request_signal_list_up=request_signal_list_up,
    #                       request_signal_list_down=request_signal_list_down,
    #                       cur_floor=cur_floor,
    #                       elevator_request_signal_list=elevator_request_signal_list)
    #     def get_upper_destination(request_signal_list_up ,
    #                               request_signal_list_down,
    #                               cur_floor,
    #                               elevator_request_signal_list ):
    #         request_upper = request_signal_list_up[cur_floor + 1:]
    #         elevator_request_signal_list_upper = elevator_request_signal_list[cur_floor + 1:]
    #         if request_upper.count(1) and elevator_request_signal_list_upper.count(1):
    #             return min(request_upper.index(1), elevator_request_signal_list_upper.index(1)) + cur_floor + 1
    #         elif (not elevator_request_signal_list_upper.count(1)) and (not request_upper.count(1)):
    #             elevator.set_direction("Down")
    #             return get_lower_destination(request_signal_list_up, request_signal_list_down, cur_floor, elevator_request_signal_list)
    #         elif not elevator_request_signal_list_upper.count(1):
    #             return request_upper.index(1) + cur_floor + 1
    #         elif not request_upper.count(1):
    #             return elevator_request_signal_list_upper.index(1) + cur_floor + 1
    #
    #     @check_has_signal(request_signal_list_up=request_signal_list_up,
    #                       request_signal_list_down=request_signal_list_down,
    #                       cur_floor=cur_floor,
    #                       elevator_request_signal_list=elevator_request_signal_list)
    #     def get_lower_destination(request_signal_list_up ,
    #                               request_signal_list_down,
    #                               cur_floor,
    #                               elevator_request_signal_list):
    #         request_lower = request_signal_list_down[0: cur_floor + 1]
    #         elevator_request_signal_list_lower = elevator_request_signal_list[0: cur_floor + 1]
    #         temp1 = request_lower[::-1]
    #         temp2 = elevator_request_signal_list_lower[::-1]
    #         if request_lower.count(1) and elevator_request_signal_list_lower.count(1):
    #             return cur_floor - min(temp1.index(1), temp2.index(1))
    #         elif (not request_lower.count(1)) and (not elevator_request_signal_list_lower.count(1)):
    #             return 0
    #         elif not request_lower.count(1):
    #             return cur_floor - temp2.index(1)
    #         elif not elevator_request_signal_list_lower.count(1):
    #             return cur_floor - temp1.index(1)
    #
    #     if elevator.direction == "up" or elevator.direction == None:
    #         destination_floor = get_upper_destination(request_signal_list_up,
    #                                                   request_signal_list_down,
    #                                                   cur_floor,
    #                                                   elevator_request_signal_list)
    #     elif elevator.direction == "down":
    #         destination_floor = get_lower_destination(request_signal_list_up,
    #                                                   request_signal_list_down,
    #                                                   cur_floor,
    #                                                   elevator_request_signal_list)
    #     print("destination_floor: ",destination_floor)
    #     return destination_floor

    def get_acceleration(self, system):
        height_floor_dict = system.building.height_floor_dict
        safety_deceleration_distance = system.elevator_safety_deceleration_distance
        accelerations = []
        for i in range(len(system.elevators)):
            elevator = system.elevators[i]
            cur_height = elevator.current_height
            cur_speed = elevator.cur_speed
            destination_floor = self.get_destination_floor(system, elevator)
            elevator.destination_floor = destination_floor
            destination_height = system.building.floor_height_dict[destination_floor]
            max_acceleration = elevator.acceleration
            max_speed = elevator.max_speed
            acceleration = self.calculate_acceleration(cur_height,
                                                  destination_height,
                                                  cur_speed,
                                                  max_acceleration,
                                                  max_speed,
                                                  safety_deceleration_distance
                                                  )
            accelerations.append(acceleration)
        return accelerations

    # def get_acceleration(self, system):
    #     height_floor_dict = system.building.height_floor_dict
    #     safety_deceleration_distance = system.elevator_safety_deceleration_distance
    #     accelerations = []
    #     for i in range(len(system.elevators)):
    #         elevator = system.elevators[i]
    #         cur_height = elevator.current_height
    #         cur_speed = elevator.cur_speed
    #         destination_floor = self.get_destination_floor(system, elevator)
    #         elevator.destination_floor = destination_floor
    #         destination_height = system.building.floor_height_dict[destination_floor]
    #         max_acceleration = elevator.acceleration
    #         max_speed = elevator.max_speed
    #         acceleration = self.calculate_acceleration(cur_height,
    #                                     destination_height,
    #                                     cur_speed,
    #                                     max_acceleration,
    #                                     max_speed,
    #                                     safety_deceleration_distance
    #                                     )
    #         accelerations.append(acceleration)
    #     return accelerations




