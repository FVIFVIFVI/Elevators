import pygame
import random
import math

imgelv = "game/images and sounds/Elevator.png"
sound1 = 'game/images and sounds/ding.mp3'

class elevator:
    screen_height = None
    pygame_initialized = False
    
    def __init__(self, screen, initialposx, floorheight, initial_ypos):
        elevator.screen_height = screen.get_height()
        elevator.pygame_initialized = True
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

    def timepass(self, current_ticks=pygame.time.get_ticks()): # Check if 2 seconds have passed since stopping
        if self.is_paused == 1:
            if current_ticks - self.pause_start_time >= 2000:
                self.is_paused = 0
                return True
            else:
                return False
        else:
            return True

    def setfloor(self, y): # Set the floor based on the y value
        adjusted_y = abs(y - self.screen_height)
        ratio_f = math.floor(adjusted_y / self.floorheight)
        if self.direction != None:
            if self.direction < 0:
                ratio_f -= 1
        return ratio_f

    def setdirection(self, floornum): # Determine if the elevator is going up or down
        if self.myfloor < floornum:
            self.direction = -1
        elif self.myfloor > floornum:
            self.direction = +1
    
    def move_elevator(self): # The function first checks how much time has passed and sets the amount of y to move relative to the elapsed time from half a second
        diftime = self.time_cul()
        speed1 = (diftime / 500) * self.floorheight * 1.1
        diftime /= 1000
        self.rect.y += self.direction * speed1
        targetfloor = self.targets[0]
        # In case we reached the floor, we need to update the new target, turn off the button, and update that we need to wait
        self.myfloor = self.setfloor(self.rect.y)
        if self.myfloor == targetfloor.floornum:
            self.dingsound.play()
            self.move_start_time = 0
            self.pause_start_time = pygame.time.get_ticks()
            self.is_paused = 1
            targetfloor.timewait = 0
            targetfloor.finish()
            self.targets.pop(0)
            self.timewait = self.time_last_check
            if self.targets:
                self.setdirection(self.targets[0].floornum)
            else:
                self.direction = None
   
    def update(self): # Decision function for different cases. The most complicated is when there are no targets but the elevator is still waiting
        if self.is_paused == 0 and not self.targets:
            self.direction = None
            self.moving = False
            return 2
        if self.targets and self.is_paused == 0:
            self.move_elevator()
        if not self.targets and self.is_paused == 1:
            self.timepass(pygame.time.get_ticks())
            self.time_cul()
        if self.targets and self.is_paused == 1:
            time_pass = self.timepass(pygame.time.get_ticks())
            if time_pass == True:
                self.move_elevator()
            else:
                self.time_cul()
        return 1

    def draw(self):
        self.screen.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(str(self.rect.y), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.y + 20))