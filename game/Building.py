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

    def __init__(self, screen, floorheight, floorwidth, numofelv=2, space=1,numfloors=17):
        self.numfloors=numfloors
        self.screen = screen
        
        self.elevators = [ElevatorFactory.create_elevator(screen, floorwidth//2 + j * 80, floorheight, (numfloors - 1) * floorheight) for j in range(numofelv)]



        self.numfloors=numfloors
        self.floors = [FloorFactory.create_floor(screen, 0, (self.numfloors - 1 - i) * floorheight, floorheight, floorwidth//2, i, self) for i in range(self.numfloors)]
        
    def update(self, floor):
        selectedelevator = self.elevators[0]
        mindistance = self.numfloors*20
        for elevator in self.elevators:
            
            if elevator.ismovingindirection(floor.floornum, elevator.direction):
                distance = abs(elevator.myfloor - floor.floornum)
                
                if distance < mindistance:
                
                    mindistance = distance
                    selectedelevator = elevator
                
        selectedelevator.addtarget(floor)
        
        #floor.timewait=mindistance*0.5
        selectedelevator.moving=True
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