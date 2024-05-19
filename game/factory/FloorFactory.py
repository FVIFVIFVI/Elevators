from objects.Floor import *
class FloorFactory:
    @staticmethod
    def create_floor(screen, posx, posy, height, width, floornum, building):
        return floor(screen, posx, posy, height, width, floornum, building)
