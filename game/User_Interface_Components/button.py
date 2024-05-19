import pygame

from abc import ABC, abstractmethod

class Button(ABC):
    def __init__(self, screen, posx, posy, width, height, text):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(posx, posy, width, height)
        self.color = (255, 255, 255)
        self.Buttonpressed = False

    @abstractmethod
    def draw(self):
        pass


    @staticmethod
    @abstractmethod
    def create_button(screen, posx, posy, width, height, text):
        pass


    def off_on(self):
        self.Buttonpressed = not self.Buttonpressed
        if self.Buttonpressed:
            self.color = (50, 205, 50)
        else:
            self.color = (255, 255, 255)

    def set_error(self):
        self.color = (255, 0, 0)

    def checkclick(self, position):
        if self.rect.collidepoint(position):
            self.off_on()
            return True
        return False

