from Passenger import Passenger
imgefloor = "b.png"
import pygame

class floor:
    def __init__(self, screen, posx, posy, height, width, floornum, building):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.floornum = floornum
        self.building = building
        self.timewait=0
        
        brickimage = pygame.image.load(imgefloor).convert_alpha()
        self.bricktexture = pygame.transform.scale(brickimage, (width, height))
        self.rect = self.bricktexture.get_rect(topleft=(posx, posy))
        self.buttonrect = pygame.Rect(posx + width - 80, posy + 10, 50, 30)
        
        
    def draw(self):
        self.screen.blit(self.bricktexture, self.rect)

        pygame.draw.ellipse(self.screen, (128, 128, 128), self.buttonrect)

        font = pygame.font.Font(None, 25)
        button_text = font.render(str(self.floornum), True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.buttonrect.center)
        self.screen.blit(button_text, button_text_rect)

        strip_height =3  
        black_strip_rect = pygame.Rect(self.posx, self.posy + self.height - strip_height, self.width, strip_height)
        pygame.draw.rect(self.screen, (0, 0, 0), black_strip_rect)  

        new_rect = pygame.Rect(self.posx + self.width - 30, self.posy , 30, 20)
        transparent_surface = pygame.Surface((new_rect.width, new_rect.height), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 128))
        self.screen.blit(transparent_surface, new_rect.topleft)

        a888 = (self.timewait) * 10
        a888 = int(a888)
        a888 /= 10
        number_text = font.render(str(a888), True, (139, 139, 0))
        number_text_rect = number_text.get_rect(center=new_rect.center)
        self.screen.blit(number_text, number_text_rect)

    def checkclick(self, position):
        if self.buttonrect.collidepoint(position):
            self.callelevator()

    def callelevator(self):
        
        self.building.update(self)