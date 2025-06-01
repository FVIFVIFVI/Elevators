class ElevatorManagementFactory:
    # Static method to create an instance of ElevatorManagement
    @staticmethod
    def create_elevator_management():
        return ElevatorManagement()


class BuildingLayout:
    def __init__(self, initial_screen_h, num_floors_val, num_elevators_val, num_buildings_requested,
                 config_floor_width, screen_width_param): # Added screen_width_param

        self.num_floors = num_floors_val
        self.num_elevators = num_elevators_val
        # self.num_buildings will be set to the actual number of buildings that fit
        self.screen_width = screen_width_param # Store screen_width
        self.screen_height = initial_screen_h  # This may be modified
        self.floor_width = config_floor_width
        
        self.bulding_loction = []
        self.building_boundaries = []
        self.bound_bulding = {}
        
        
        actual_buildings_that_fit = 0
        # Calculate positions and check if they fit horizontally
        for i in range(num_buildings_requested): 
            # 'A' is the start_x of the current building
            start_x = (self.floor_width // 2 + self.num_elevators * 80 + 40) * i 
            
            if start_x + self.floor_width <= self.screen_width:
                self.bulding_loction.append(start_x)
                boundary_data = {
                    'x1': start_x,
                    'y': 0, # y is part of the original structure, kept.
                    'x2': start_x + self.floor_width,
                }
                self.building_boundaries.append(boundary_data)
                actual_buildings_that_fit += 1
            else:
                # Stop if a building doesn't fit; further buildings also won't.
                self.bound_bulding["error"] = f"Building does not fit the last building is {i}"
                break 
        self.num_buildings = actual_buildings_that_fit # The actual number of buildings created

        # Adjust screen_height based on max floor height constraint
        if self.num_floors > 0:
            if self.screen_height / self.num_floors > 110:
                self.screen_height = 110 * self.num_floors
            # User comment: #צריך להוסיף לוגיקה למינימום (Need to add logic for minimum)
            # Minimum logic not added as per "לא להוסיף תיקונים שלא ביקשתי"
        # else: screen_height remains initial_screen_h if num_floors is not positive.

        # Calculate floor_height
        if self.num_floors > 0:
            self.floor_height = self.screen_height / self.num_floors
        else:
            self.floor_height = 0 # Default if no floors or invalid number

        # The second loop for building_boundaries from user's code is now integrated into the first loop.

        # For get_total_width_needed and get_final_building_height consistency
        self.stride_width_per_building = (self.floor_width // 2 + self.num_elevators * 80 + 40) # User's unit for offset calculation
        self.final_building_height = self.screen_height # Assuming this is what was intended

    def get_floor_height(self):
        return self.floor_height

    def get_final_building_height(self):
        # self.final_building_height is set in __init__ to self.screen_height
        return self.final_building_height 

    def get_building_offset(self, building_index): # Renamed from get_building_boundaries to match usage
        if 0 <= building_index < len(self.building_boundaries):
            return self.building_boundaries[building_index] # Returns the dict {'x1': ..., 'x2': ...}
        return None # Fallback if index is out of bounds

    def get_total_width_needed(self):
        if not self.building_boundaries:
            return 0
        # The total width is the x-coordinate of the end of the last building.
        # Assuming bulding_loction contains start positions.
        last_building_boundary = self.building_boundaries[-1]
        return last_building_boundary['x2']
        # Or, based on user's stride idea:
        # if self.num_buildings == 0:
        #    return 0
        # return self.stride_width_per_building * (self.num_buildings -1) + self.floor_width
        # The self.building_boundaries[-1]['x2'] is more direct from the calculated data.
        
    

    def WHERE_IS_POSITION(self, x, y): # y is not used by this specific boundary check
        low = 0
        high = len(self.building_boundaries) - 1
        
        if not self.building_boundaries:
            return None # No buildings to search within

        # Binary search for the building index
        while low <= high:
            mid = (low + high) // 2
            building_data = self.building_boundaries[mid]
            if building_data['x1'] <= x < building_data['x2']: # x is within [x1, x2)
                return mid # Return the index of the building
            elif x < building_data['x1']:
                high = mid - 1
            else: # x >= building_data['x2']
                low = mid + 1
        
        return None # Not found in any building
    
    