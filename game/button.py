import pygame
from ImageFactory import ImageFactory

class Button:
    def __init__(self, screen, posx, posy, width, height, text, shape="rect"):
        self.screen = screen
        self.posx = posx
        self.posy = posy-5
        self.width = width
        self.height = height
        self.text = text
        self.shape = shape
        self.rect = pygame.Rect(posx, posy-5, width, height)
        self.c = (255, 255, 255)
        self.Buttonpressed = False

    def set_shape(self):
        if self.shape == "rect":
            return pygame.draw.rect
        elif self.shape == "ellipse":
            return pygame.draw.ellipse

    def draw(self):
        
            
        
        shape_surface = ImageFactory.create_ellipse_surface(self.width, self.height, (128, 128, 128))
        
        self.screen.blit(shape_surface, (self.posx, self.posy))
        
        font = pygame.font.Font(None, 25)
        button_text = font.render(str(self.text), True, self.c)
        button_text_rect = button_text.get_rect(center=self.rect.center)
        self.screen.blit(button_text, button_text_rect)

    def off_on(self):
        self.Buttonpressed = not self.Buttonpressed
        if self.Buttonpressed:
            self.c = (50, 205, 50)
        else:
            self.c = (255, 255, 255)

    def checkclick(self, position):
        if self.rect.collidepoint(position):
            if not self.Buttonpressed:
                self.off_on()
                return True
        return False

class ButtonFactory:
    @staticmethod
    def create_button(screen, posx, posy, width, height, text, shape="rect"):
        return Button(screen, posx, posy, width, height, text, shape)
