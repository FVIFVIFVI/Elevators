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
        #self.elevators = [elevator(screen, p+floorwidth//2 + j * 80, floorheight, (numfloors - 1) * floorheight) for j in range(numofelv)]
        self.elevators = [self.create_elevator(p + floorwidth//2 + j * 80, floorheight, (numfloors - 1) * floorheight) for j in range(numofelv)]
        self.elevatorsmove = []
        self.floors = [self.create_floor(0 + p, (self.numfloors - 1 - i) * floorheight, floorheight, floorwidth//2, i) for i in range(self.numfloors)]
        self.numfloors=numfloors
       # self.floors = [floor(screen, 0+p, (self.numfloors - 1 - i) * floorheight, floorheight, floorwidth//2, i, self) for i in range(self.numfloors)]

    def create_floor(self, posx, posy, height, width, floornum):
        return FloorFactory.create_floor(self.screen, posx, posy, height, width, floornum, self)

    def create_elevator(self, initialposx, floorheight, initial_ypos):
        return ElevatorFactory.create_elevator(self.screen, initialposx, floorheight, initial_ypos)


    def update(self, floor):
        selectedelevator = self.elevators[0]
        mindistance = self.numfloors*20
        for elevator in self.elevators:
            if elevator.myfloor==floor.floornum:
                return True
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
            

    def draw(self):
        for floor in self.floors:
            floor.draw()
        for elevator in self.elevators:
            elevator.draw()