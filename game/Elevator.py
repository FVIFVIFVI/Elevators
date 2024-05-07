import pygame
import random
import math
imgelv = "elv.png"
sound1 = 'ding.mp3'
class elevator:
    screen1=None
    pygame_initialized = False
    def __init__(self, screen, initialposx, floorheight, initial_ypos):
        elevator.screen1=  (pygame.display.Info()).current_h
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
        self.timewait=0#לזכור לאפס
        
    def addtarget(self, floor,sum):
        
        if floor not in self.targets:
            self.targets.append(floor)
            
            
        if self.direction is None:
            self.setdirection(floor.floornum)
        floor.timewait=sum
        

    def opt(self, targets, current_floor, new_floor):
        if not targets:
            return abs(current_floor - new_floor)*0.5
        return targets[-1].timewait + 2 + abs(targets[-1].floornum - new_floor)#maybe for

    
    def timepass(self,current_ticks):
        if self.pusze == 1:
                
                if current_ticks - self.time1 >= 2000:
                    self.pusze = 0
                return False
        else:
                return True

    
    def setfloor(self,y):
        adjusted_y = abs(y - self.screen1)
        a = math.floor(adjusted_y / self.floorheight)
        if self.direction!=None:
            if self.direction < 0:
                a -= 1
        return a
    
    def setdirection(self, floornum):
        if self.myfloor < floornum:
            self.direction = -1
        elif self.myfloor > floornum:
            self.direction = +1

    def move(self):
        p=False
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
        if self.timepass(current_ticks):
            self.rect.y += self.direction * speed1
            

        for target in self.targets:#עובד רק בגיקסה הפשוטה
            
            target.timewait -= diftime
        
          
        self.myfloor=self.setfloor(self.rect.y)

        if self.myfloor == targetfloor.floornum:
            self.dingsound.play()
            self.time2 = 0
            self.time1 = current_ticks
            self.pusze = 1
            targetfloor.timewait = 0
            targetfloor.finish()
            self.targets.pop(0)
            
            
            if not self.targets:
                self.direction = None
                self.moving = False

            else:
                self.setdirection(self.targets[0].floornum)



    # def ismovingindirection(self, floornum, direction):
        
    #     if self.direction is None:
    #         return True
    #     return (self.direction == 1 and self.myfloor > floornum) or (self.direction == -1 and self.myfloor < floornum)
   
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

        