from objects.Elevator import *

class ElevatorFactory:
    @staticmethod
    def create_elevator(screen, initialposx, floorheight, initial_ypos):
        return elevator(screen, initialposx, floorheight, initial_ypos)
