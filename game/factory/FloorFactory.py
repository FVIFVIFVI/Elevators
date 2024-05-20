from objects.Floor import *

class FloorFactory:
    @staticmethod
    def create_floor(screen, posx, posy, height, width, floornum, building):
        return Floor(screen, posx, posy, height, width, floornum, building)


