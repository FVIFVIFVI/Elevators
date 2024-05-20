import pygame
from factory.ShapeFactory import *


class Button:
    def __init__(self, screen, posx, posy, width, height, text, shape="rect"):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.text = text
        self.shape = shape
        self.rect = pygame.Rect(posx, posy, width, height)
        self.c = (255, 255, 255)
        self.Buttonpressed = False
        self.active = False
    

    def draw(self):
        shape_surface = ShapeFactory.create_shape(self.shape, width=self.width, height=self.height, color=(128, 128, 128))
        self.screen.blit(shape_surface, (self.posx, self.posy))
        font = pygame.font.Font(None, 25)
        button_text = font.render(str(self.text), True, self.c)
        button_text_rect = button_text.get_rect(center=self.rect.center)
        self.screen.blit(button_text, button_text_rect)


    #light switch
    def off_on(self):
        self.Buttonpressed = not self.Buttonpressed
        if self.Buttonpressed:
            self.c = (50, 205, 50)
        else:
            self.c = (255, 255, 255)


    #A case of an error in elevator allocation
    def set_error(self):
        self.c = (255, 0, 0)


    def checkclick(self, position):
        if self.rect.collidepoint(position):
            if not self.Buttonpressed:
                self.off_on()
                return True
        return False
