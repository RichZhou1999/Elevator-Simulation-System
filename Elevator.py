from Controller import Controller

'''

state: wait or running

'''


class Elevator:
    def __init__(self, capacity, max_speed, controller):
        self.capacity = capacity
        self.max_speed = max_speed
        self.controller = controller
        self.cur_speed = 0
        self.acceleration = 0
        self.current_accommodation = 0
        self.current_height = 0
        self.state = "wait"
        self.cur_waited_time = 0
        self.destination = None

    def update(self, system):
        simulation_step = system.simulation_step
        self.adjust_acceleration()
        self.adjust_height(simulation_step)
        self.adjust_speed(simulation_step)

    def adjust_acceleration(self, system):
        self.acceleration = self.controller.get_acceleration(system)

    def adjust_speed(self, simulation_step):
        self.cur_speed += self.acceleration * simulation_step

    def adjust_height(self, simulation_step):
        self.current_height = self.current_height +\
                              self.cur_speed * simulation_step + self.acceleration/2*simulation_step**2


