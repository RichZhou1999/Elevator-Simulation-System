from abc import ABCMeta, abstractmethod

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

"add new controllers and algorithms here"
class XXXController(Controller):
    pass

class Controller_one_elevator(Controller):
    def get_acceleration(self, system):
        height_floor_dict = system.building.height_floor_dict
