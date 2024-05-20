from factory.FloorFactory import *
from factory.ElevatorFactory import *

class Building:
    def __init__(self, screen, floor_height, floor_width, num_of_elevators=2, space=1, num_floors=25, offset=0):
        self.num_floors = num_floors
        self.screen = screen
        self.elevators = [ElevatorFactory.create_elevator(screen, offset + floor_width // 2 + j * 80, floor_height, (num_floors - 1) * floor_height) for j in range(num_of_elevators)]
        self.elevators_move = []
        self.floors = [FloorFactory.create_floor(screen, 0 + offset, (self.num_floors - 1 - i) * floor_height, floor_height, floor_width // 2, i, self) for i in range(self.num_floors)]
        self.locate_floor = {i: floor for i, floor in enumerate(self.floors)}
        self.init_params = [screen, floor_height, floor_width, num_of_elevators, space, num_floors, offset]  # Saved for reset purposes
    

    #Returns the simulation to the beginning
    def reset_elevators(self):
        screen, floor_height, floor_width, num_of_elevators, space, num_floors, offset = self.init_params
        self.elevators = [ElevatorFactory.create_elevator(screen, offset + floor_width // 2 + j * 80, floor_height, (num_floors - 1) * floor_height) for j in range(num_of_elevators)]


    # Find minimum using the opt function
    def choose_optimal_elevator(self, floor):
        selected_elevator = None
        min_wait_time = float('inf')
        for elev in self.elevators:
            if elev.myfloor == floor.floornum and elev.direction is None:
                return 1  # If the elevator is not moving and already at the floor, there's an elevator here
            wait_time = elev.opt(elev.targets, elev.myfloor, floor.floornum)
            if wait_time < min_wait_time:
                min_wait_time = wait_time
                selected_elevator = elev
        if selected_elevator is None:
            return 2  # In case there are no elevators, we do not enter the for loop
        
        # Add to the target list of the selected elevator
        # Additionally, we pass the arrival time calculated by opt
        selected_elevator.addtarget(floor, min_wait_time)
        if not selected_elevator.moving:  # We have a list of elevators that need to move, so we avoid going over all irrelevant elevators
            self.elevators_move.append(selected_elevator)
        selected_elevator.moving = True
        selected_elevator.move_start_time = 0  # This is a helper variable that needs to be reset initially


    # Update function for what happens in the building
    def update(self):
        for elev in self.elevators_move:
            if elev.update() == 2:
                self.elevators_move.remove(elev)  # If the elevator has completed its task, it is removed from the list


    def draw(self):
        for floor in self.floors:
            floor.draw()
        for elev in self.elevators:
            elev.draw()
