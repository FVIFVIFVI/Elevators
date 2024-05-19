from objects.Building import *
class BuildingFactory:
    @staticmethod
    def create_building(screen, floor_height, floor_width, num_of_elevators=2, space=1, num_floors=25, offset=0):
        return Building(screen, floor_height, floor_width, num_of_elevators, space, num_floors, offset)