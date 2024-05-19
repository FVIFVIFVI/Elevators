from User_Interface_Components.button import *

class RectButton(Button):
    def draw(self):
        pygame.draw.rect(self.screen, (128, 128, 128), self.rect)
        
        font = pygame.font.Font(None, 25)
        button_text = font.render(str(self.text), True, self.color)
        button_text_rect = button_text.get_rect(center=self.rect.center)
        self.screen.blit(button_text, button_text_rect)

    @staticmethod
    def create_button(screen, posx, posy, width, height, text):
        return RectButton(screen, posx, posy, width, height, text)

class EllipseButton(Button):
    def draw(self):
        pygame.draw.ellipse(self.screen, (128, 128, 128), self.rect)
        
        font = pygame.font.Font(None, 25)
        button_text = font.render(str(self.text), True, self.color)
        button_text_rect = button_text.get_rect(center=self.rect.center)
        self.screen.blit(button_text, button_text_rect)

    @staticmethod
    def create_button(screen, posx, posy, width, height, text):
        return EllipseButton(screen, posx, posy, width, height, text)