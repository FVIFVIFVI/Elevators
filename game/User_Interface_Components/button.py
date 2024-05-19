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
        self.c = (255, 255, 255)
        self.Buttonpressed = False
        self.active = False
    
    def set_shape(self):
        if self.shape == "rect":
            return pygame.draw.rect
        elif self.shape == "ellipse":
            return pygame.draw.ellipse

    def draw(self):
        dshape = self.set_shape()
        dshape(self.screen, (128, 128, 128), self.rect)
        
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

    def set_error(self):
        self.c = (255, 0, 0)

    def checkclick(self, position):
        if self.rect.collidepoint(position):
            if not self.Buttonpressed:
                self.off_on()
            return True
        return False
