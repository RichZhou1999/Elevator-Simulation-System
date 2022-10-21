from abc import ABCMeta, abstractmethod
import bisect

'''

'''
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
                               max_speed):
        acceleraion = 0
        delta_height = destination_height - cur_height
        if cur_speed == 0:
            if delta_height > 0:
                return max_acceleration
            elif delta_height < 0:
                return -max_acceleration
            else:
                return 0
        deacceleration_distance = 0.5 * cur_speed**2 / max_acceleration
        if abs(delta_height) > deacceleration_distance:
            if abs(cur_speed) < max_speed:
                acceleraion = max_acceleration
            elif abs(cur_speed) == max_speed:
                acceleraion = 0
        elif abs(delta_height) <= deacceleration_distance:
            acceleraion = max_acceleration * - cur_speed / abs(cur_speed)
        return acceleraion


"add new controllers and algorithms here"
class XXXController(Controller):
    pass

class Controller_one_elevator(Controller):

    def get_destination_floor(self, system, elevator):
        request_signal_list_up = system.request_signal_list_up
        request_signal_list_down = system.request_signal_list_down
        cur_height = elevator.current_height
        floor_height_list = system.building.height_floor_dict.keys()
        cur_floor = bisect.bisect_right(floor_height_list, cur_height) - 1
        def check_has_signal(request_signal_list_up , request_signal_list_down):
            def inner(f, *args, **kwargs):
                return f(*args, **kwargs)
            def zero():
                return 0
            if request_signal_list_up.count(1) == 0 and request_signal_list_down == 0:
                return zero
            else:
                return inner

        @check_has_signal(request_signal_list_up, request_signal_list_down, cur_floor)
        def get_upper_destination(request_signal_list_up , request_signal_list_down, cur_floor):
            request_upper = request_signal_list_up[cur_floor + 1:]
            if request_upper.count(1):
                return request_upper.index(1) + cur_floor + 1
            else:
                elevator.set_direction("Down")
                return get_lower_destination(request_signal_list_up, request_signal_list_down, cur_floor)

        @check_has_signal(request_signal_list_up, request_signal_list_down, cur_floor)
        def get_lower_destination(request_signal_list_up , request_signal_list_down, cur_floor):
            request_lower = request_signal_list_down[0: cur_floor + 1]
            if request_lower.count(1):
                temp = request_lower[::-1]
                return cur_floor - temp.index(1)


        if elevator.direction == "Up" or elevator.direction == "None":
            destination_floor = get_upper_destination()
        elif elevator.direction == "Down":
            destination_floor = get_lower_destination()
        return destination_floor



    def get_acceleration(self, system):
        height_floor_dict = system.building.height_floor_dict
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
            self.calculate_acceleration(cur_height,
                                        destination_height,
                                        cur_speed,
                                        max_acceleration,
                                        max_speed
                                        )



