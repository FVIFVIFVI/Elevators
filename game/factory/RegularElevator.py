from objects_abstract.Elevator import *

class RegularElevator(Elevator):
    
    @staticmethod
    def create_elevator(screen, initialposx, floorheight, initial_ypos):
        return RegularElevator(screen, initialposx, floorheight, initial_ypos)

    def move_elevator(self):
        # The function first checks how much time has passed and sets the amount of y to move relative to the elapsed time from half a second
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

    def update(self):
        # Decision function for different cases. The most complicated is when there are no targets but the elevator is still waiting
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
        self.screen.blit(text_surface, text_rect)
