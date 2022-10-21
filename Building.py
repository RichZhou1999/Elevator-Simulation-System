class Building:
    def __init__(self, height_floor_dict):
        self.height_floor_dict = height_floor_dict
        self.floor_height_dict = dict((v, k) for k, v in self.height_floor_dict.items())
