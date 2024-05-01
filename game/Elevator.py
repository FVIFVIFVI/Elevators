import pygame
import random
import math
imgelv = "elv.png"
a88=0
sound1 = 'ding.mp3'
class elevator:
    def __init__(self, screen, initialposx, floorheight, initial_ypos):
        self.screen = screen
        self.ypos = initial_ypos
        self.xpos = initialposx
        self.floorheight = floorheight
        self.step = floorheight / 100
        self.myfloor = 0
        self.direction = None
        self.targets = []
        self.passengers = []
        self .pusze=0
        pygame.mixer.init()
        self.dingsound = pygame.mixer.Sound(sound1)
        self.moving = False
        self.time1=0
        self.time2=0
        self.time3=pygame.time.get_ticks()
        originalimage = pygame.image.load(imgelv).convert_alpha()
        self.image = pygame.transform.scale(originalimage, (75, int(floorheight * 0.75)))
        self.rect = self.image.get_rect(topleft=(self.xpos, self.ypos))
        
    def addtarget(self, floor):
        
        if floor not in self.targets:
            self.targets.append(floor)
            self.targets.sort(key=lambda x: x.floornum, reverse=self.direction == 1)
        if self.direction is None:
            self.setdirection(floor.floornum)
        floor.timewait=self.calculate_wait_time(self.targets,self.myfloor,floor.floornum,self.direction)
    
    def calculate_wait_time(self,targets, current_floor, new_floor, direction):
        
        initial_distance = abs(current_floor - new_floor)
        initial_wait_time = initial_distance * 0.5
        index = 0
        if direction == 1:
            while index < len(targets) and targets[index].floornum > new_floor:
                index += 1
        else:
            while index < len(targets) and targets[index].floornum < new_floor:
                index += 1
        
        additional_wait_time = 2 * index
        
        return initial_wait_time + additional_wait_time




    

    def setdirection(self, floornum):
        if self.myfloor < floornum:
            self.direction = -1
        elif self.myfloor > floornum:
            self.direction = +1

    def move(self, dt):
        if self.time2 == 0:
            self.time3 = pygame.time.get_ticks()
            self.time2 = 1

        current_ticks = pygame.time.get_ticks()
        diftime = current_ticks - self.time3
        speed1 = (diftime / 500) * self.floorheight
        self.time3 = current_ticks

        if not self.targets:
            return
        if self.direction is None:
            return

        targetfloor = self.targets[0]
        diftime /= 1000
        if self.pusze == 1:
            
            if current_ticks - self.time1 >= 2000:
                self.pusze = 0
        else:
            self.rect.y += self.direction * speed1
           

        for target in self.targets:#עובד רק בגיקסה הפשוטה
            
            target.timewait -= diftime
        
        adjusted_y = abs(self.rect.y - 1000)  
        self.myfloor = math.floor(adjusted_y / self.floorheight)

        if self.direction < 0:
            self.myfloor -= 1

        if self.myfloor == targetfloor.floornum:
            self.dingsound.play()
            self.time2 = 0
            self.time1 = current_ticks
            self.pusze = 1
            targetfloor.timewait = 0
            self.targets.pop(0)
            if not self.targets:
                self.direction = None
                self.moving = False



    def ismovingindirection(self, floornum, direction):
        
        if self.direction is None:
            return True
        return (self.direction == 1 and self.myfloor > floornum) or (self.direction == -1 and self.myfloor < floornum)
    if a88==0:
        def ismovingindirection(self, floornum,a):
            if self.direction is None:
                return True

        
            if self.direction == 1:
            
                return floornum < self.targets[-1].floornum

            
            elif self.direction == -1:
            
                return floornum > self.targets[-1].floornum

    

    


    def draw(self):
        self.screen.blit(self.image, self.rect)

        font = pygame.font.Font(None, 36)  

        text_surface = font.render(str(self.rect.y), True, (0, 0, 0))  
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.y + 20))  

        