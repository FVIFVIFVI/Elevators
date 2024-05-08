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

    def __init__(self, screen, floorheight, floorwidth, numofelv=2, space=1, numfloors=25, p=0):
        self.numfloors = numfloors
        self.screen = screen
        self.elevators = [self.create_elevator(p + floorwidth//2 + j * 80, floorheight, (numfloors - 1) * floorheight) for j in range(numofelv)]
        self.elevatorsmove = []
        self.floors = [self.create_floor(0 + p, (self.numfloors - 1 - i) * floorheight, floorheight, floorwidth//2, i) for i in range(self.numfloors)]
        self.locatefloor = {i: floor for i, floor in enumerate(self.floors)}
        self.init_params = [screen, floorheight, floorwidth, numofelv, space, numfloors, p]
    
    def create_floor(self, posx, posy, height, width, floornum):
        return FloorFactory.create_floor(self.screen, posx, posy, height, width, floornum, self)

    def create_elevator(self, initialposx, floorheight, initial_ypos):
        return ElevatorFactory.create_elevator(self.screen, initialposx, floorheight, initial_ypos)
    
    # def restelv(self):
    #     screen, floorheight, floorwidth, numofelv, space, numfloors, p = self.init_params
    #     self.elevators=[]
    #     self.elevators = [elevator(screen, p+floorwidth//2 + j * 80, floorheight, (numfloors - 1) * floorheight) for j in range(numofelv)]

    def restelv(self):
        screen, floorheight, floorwidth, numofelv, space, numfloors, p = self.init_params
        self.elevators =[]
        self.elevators = [self.create_elevator(p+floorwidth//2 + j * 80, floorheight, (numfloors - 1) * floorheight) for j in range(numofelv)]

    def update(self, floor):
        selectedelevator = None
        minwaittime = float('inf')
        for elev in self.elevators:
            if elev.myfloor==floor.floornum:
                return True
            wait_time = elev.opt(elev.targets, elev.myfloor, floor.floornum)
            if wait_time < minwaittime:
                minwaittime = wait_time
                selectedelevator = elev
        
        if selectedelevator:
            selectedelevator.addtarget(floor, minwaittime)
            if not selectedelevator.moving:
                self.elevatorsmove.append(selectedelevator)
            selectedelevator.moving = True

    def update1(self):
        for i in self.elevatorsmove:
            if i.moving:
                i.move()
            else:
                self.elevatorsmove.remove(i)
            i.draw()

    def draw(self):
        for floor in self.floors:
            floor.draw()
        for elevator in self.elevators:
           
             elevator.draw()
