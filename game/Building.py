from Elevator import elevator
from Floor import floor

class FloorFactory:
    @staticmethod
    def create_floor(screen, posx, posy, height, width, floornum, building):
        return floor(screen, posx, posy, height, width, floornum, building)

class ElevatorFactory:
    @staticmethod
    def create_elevator(screen, initialposx, floorheight, initial_ypos):
        return elevator(screen, initialposx, floorheight, initial_ypos)

class building:

    def __init__(self, screen, floorheight, floorwidth, numofelv=2, space=1,numfloors=25,p=0):
        self.numfloors=numfloors
        self.screen = screen
        self.elevators = [elevator(screen, p+floorwidth//2 + j * 80, floorheight, (numfloors - 1) * floorheight) for j in range(numofelv)]


        self.numfloors=numfloors
        self.floors = [floor(screen, 0+p, (self.numfloors - 1 - i) * floorheight, floorheight, floorwidth//2, i, self) for i in range(self.numfloors)]

        
    def update(self, floor):
        selectedelevator = None
        minwaittime = float('inf')  # Initialize with a very large number
       
        for elev in self.elevators:
            wait_time = elev.opt(elev.targets, elev.myfloor, floor.floornum)
            print(wait_time,elev.myfloor)
            if wait_time < minwaittime:
                minwaittime = wait_time
                selectedelevator = elev
        
        if selectedelevator:
            selectedelevator.addtarget(floor,minwaittime)
            selectedelevator.moving = True
    def update1(self,dt):
        for i in self.elevators:
            
            if i.moving==True:
              i.move(dt)
            i.draw()

    def draw(self):
        for floor in self.floors:
            floor.draw()
        for elevator in self.elevators:
            elevator.draw()