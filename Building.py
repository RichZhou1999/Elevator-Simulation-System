class Building:
    def __init__(self, height_floor_dict):
        # {height: floor}
        self.height_floor_dict = height_floor_dict
        # {floor: height}
        self.floor_height_dict = dict((v, k) for k, v in self.height_floor_dict.items())
