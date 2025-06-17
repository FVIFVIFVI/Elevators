class ElevatorManagementFactory:
    @staticmethod
    def create_elevator_management():
        return ElevatorManagement()


class BuildingLayout:
    def __init__(self, initial_screen_h, num_floors_val, num_elevators_val, num_buildings_requested,
                 config_floor_width, screen_width_param):
        self.num_floors = num_floors_val
        self.num_elevators = num_elevators_val
        self.screen_width = screen_width_param
        self.screen_height = initial_screen_h
        self.floor_width = config_floor_width
        
        self.bulding_loction = []
        self.building_boundaries = []
        self.bound_bulding = {}
        
        actual_buildings_that_fit = 0
        for i in range(num_buildings_requested):
            start_x = (self.floor_width // 2 + self.num_elevators * 80 + 40) * i
            
            if start_x + self.floor_width <= self.screen_width:
                self.bulding_loction.append(start_x)
                boundary_data = {
                    'x1': start_x,
                    'y': 0,
                    'x2': start_x + self.floor_width,
                }
                self.building_boundaries.append(boundary_data)
                actual_buildings_that_fit += 1
            else:
                self.bound_bulding["error"] = f"Building does not fit the last building is {i}"
                break
        self.num_buildings = actual_buildings_that_fit

        if self.num_floors > 0:
            if self.screen_height / self.num_floors > 110:
                self.screen_height = 110 * self.num_floors
        
        if self.num_floors > 0:
            self.floor_height = self.screen_height / self.num_floors
        else:
            self.floor_height = 0

        self.stride_width_per_building = (self.floor_width // 2 + self.num_elevators * 80 + 40)
        self.final_building_height = self.screen_height

    def get_floor_height(self):
        return self.floor_height

    def get_final_building_height(self):
        return self.final_building_height

    def get_building_offset(self, building_index):
        if 0 <= building_index < len(self.building_boundaries):
            return self.building_boundaries[building_index]
        return None

    def get_total_width_needed(self):
        if not self.building_boundaries:
            return 0
        last_building_boundary = self.building_boundaries[-1]
        return last_building_boundary['x2']
        
    def WHERE_IS_POSITION(self, x, y):
        low = 0
        high = len(self.building_boundaries) - 1
        
        if not self.building_boundaries:
            return None

        while low <= high:
            mid = (low + high) // 2
            building_data = self.building_boundaries[mid]
            if building_data['x1'] <= x < building_data['x2']:
                return mid
            elif x < building_data['x1']:
                high = mid - 1
            else:
                low = mid + 1
        
        return None