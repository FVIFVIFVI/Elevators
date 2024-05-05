import pygame

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

    def set_shape(self):
        if self.shape == "rect":
            return pygame.draw.rect
        elif self.shape == "ellipse":
            return pygame.draw.ellipse

    def draw(self):
        # dshape = getattr(pygame.draw, self.shape)
        # dshape(self.screen, (128, 128, 128), self.rect)
        dshape = self.set_shape()
        dshape(self.screen, (128, 128, 128), self.rect)
        
        font = pygame.font.Font(None, 25)
        button_text = font.render(str(self.text), True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.rect.center)
        self.screen.blit(button_text, button_text_rect)
        
    def checkclick(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

class ButtonFactory:
    @staticmethod
    def create_button(screen, posx, posy, width, height, text, shape="rect"):
        return Button(screen, posx, posy, width, height, text, shape)






