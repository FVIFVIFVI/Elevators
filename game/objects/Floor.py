from factory.ShapeFactory import ShapeFactory
from factory.ButtonFactory import ButtonFactory
import pygame

image_floor = 'game/images and sounds/floor.png'

class Floor:
    def __init__(self, screen, posx, posy, height, width, floornum, building):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.floornum = floornum
        self.building = building
        self.timewait = 0
        self.bricktexture = ShapeFactory.create_shape('image', image_path=image_floor, width=width, height=height)
        self.rect = self.bricktexture.get_rect(topleft=(posx, posy))
        new_rect = pygame.Rect(posx + width - 30, posy, 30, 20)
        self.transparent_surface = ShapeFactory.create_shape('transparent_surface', width=new_rect.width, height=new_rect.height, alpha=128)
        self.transparent_surface_rect = self.transparent_surface.get_rect(topleft=new_rect.topleft)
        self.black_strip_rect = pygame.Rect(posx, posy + height - 3, width, 3)
        
        #Calculation of button position
        button_width, button_height = width // 2, int(height * 0.7)
        free_width = width - new_rect.width - 2
        posxb = posx + (free_width - button_width)
        posyb = posy + (height - button_height) // 2
        self.button = ButtonFactory.create_button(screen, posxb, posyb, button_width, button_height, str(floornum), shape="ellipse")


    def draw(self):
        self.screen.blit(self.bricktexture, self.rect)
        self.button.draw()
        pygame.draw.rect(self.screen, (0, 0, 0), self.black_strip_rect)
        self.screen.blit(self.transparent_surface, self.transparent_surface_rect.topleft)
        rounded_wait_time = round(self.timewait, 1)
        font = pygame.font.Font(None, 25)
        number_text = font.render(str(rounded_wait_time), True, (139, 139, 0))
        number_text_rect = number_text.get_rect(center=self.transparent_surface_rect.center)
        self.screen.blit(number_text, number_text_rect)
    
    
    #check event from user
    def checkclick(self, position):
        if self.button.checkclick(position):
            self.call_elevator()


    def call_elevator(self):
        answer_from_building = self.building.choose_optimal_elevator(self)
        if answer_from_building == 1:
            self.button.off_on()
        elif answer_from_building == 2:
            self.button.set_error()
    

    #Turn off button lighting
    def finish(self):
        self.button.off_on()
