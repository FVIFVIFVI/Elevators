import pygame
import random
import math
from abc import ABC, abstractmethod

imgelv = "game/images and sounds/Elevator.png"
sound1 = 'game/images and sounds/ding.mp3'

class Elevator(ABC):
    screen_height = None
    pygame_initialized = False
    
    def __init__(self, screen, initialposx, floorheight, initial_ypos):
        Elevator.screen_height = screen.get_height()
        Elevator.pygame_initialized = True
        self.screen = screen
        self.ypos = initial_ypos
        self.xpos = initialposx
        self.floorheight = floorheight
        self.step = floorheight / 100
        self.myfloor = 0
        self.direction = None
        self.targets = []
        self.passengers = []
        self.is_paused = 0
        pygame.mixer.init()
        self.dingsound = pygame.mixer.Sound(sound1)
        self.moving = False
        self.pause_start_time = 0
        self.move_start_time = 0
        self.time_last_check = pygame.time.get_ticks()
        originalimage = pygame.image.load(imgelv).convert_alpha()
        self.image = pygame.transform.scale(originalimage, (75, int(floorheight * 0.75)))
        self.rect = self.image.get_rect(topleft=(self.xpos, self.ypos))
        self.timewait = 0

    def addtarget(self, floor, sum):
        # 1. Set the wait time for the calling floor
        # 2. Determine the direction to know whether to add or subtract when adding a target
        if floor not in self.targets:
            self.targets.append(floor)
        if self.direction is None:
            self.setdirection(floor.floornum)
        if not self.targets and self.is_paused == 0:
            self.move_start_time = 0
        floor.timewait = sum

    def opt(self, targets, current_floor, new_floor):
        # If there are no targets, first check if 2 seconds have passed since the elevator stopped.
        # If not, add the time. Otherwise, the optimal time is the optimal time of the last stop -> opt(n) = opt(n-1) + 2 + dist
        if not targets:
            temptime = pygame.time.get_ticks()
            dift = 2 - ((temptime - self.pause_start_time) / 1000)
            temp = 0
            if dift > 0 and dift <= 2:
                temp = dift
            return abs(current_floor - new_floor) * 0.5 + temp
        return targets[-1].timewait + 2 + abs(targets[-1].floornum - new_floor)

    def time_cul(self, index=0):
        current_ticks = pygame.time.get_ticks()
        # Set the start time of the function run
        if self.move_start_time == 0:
            self.time_last_check = pygame.time.get_ticks()
            self.move_start_time = 1
        
        diftime = current_ticks - self.time_last_check
        self.time_last_check = current_ticks
        diftime /= 1000
        # Update the waiting time for all floors during the elapsed time
        for target in self.targets[index:]:
            target.timewait -= diftime
        return diftime * 1000

    def timepass(self, current_ticks=pygame.time.get_ticks()): 
        # Check if 2 seconds have passed since stopping
        if self.is_paused == 1:
            if current_ticks - self.pause_start_time >= 2000:
                self.is_paused = 0
                return True
            else:
                return False
        else:
            return True

    def setfloor(self, y): 
        # Set the floor based on the y value
        adjusted_y = abs(y - self.screen_height)
        ratio_f = math.floor(adjusted_y / self.floorheight)
        if self.direction != None:
            if self.direction < 0:
                ratio_f -= 1
        return ratio_f

    def setdirection(self, floornum): 
        # Determine if the elevator is going up or down
        if self.myfloor < floornum:
            self.direction = -1
        elif self.myfloor > floornum:
            self.direction = +1

    @abstractmethod
    def move_elevator(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

