from button import ButtonFactory
from ImageFactory import *
from button import ButtonFactory
from ImageFactory import *
imgefloor = "b.png"

class floor:
    def __init__(self, screen, posx, posy, height, width, floornum, building):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.floornum = floornum
        self.building = building
        self.timewait = 0
        self.bricktexture = ImageFactory.create_image(imgefloor, width, height)
        self.timewait = 0
        self.bricktexture = ImageFactory.create_image(imgefloor, width, height)
        self.rect = self.bricktexture.get_rect(topleft=(posx, posy))
        posxb,posyb=posx + width - 80,posy + 10
        self.button = ButtonFactory.create_button(screen, posxb,posyb , width//2, height*0.7, str(self.floornum), shape="ellipse")
        new_rect = pygame.Rect(self.posx + self.width - 30, self.posy, 30, 20)
        self.transparent_surface = ImageFactory.create_transparent_surface(new_rect.width, new_rect.height, 128)
        self.transparent_surface_rect = self.transparent_surface.get_rect(topleft=new_rect.topleft)
        self.black_strip_rect = ImageFactory.create_rect(self.posx, self.posy + self.height - 3, self.width, 3)

        posxb,posyb=posx + width - 80,posy + 10
        self.button = ButtonFactory.create_button(screen, posxb,posyb , width//2, height*0.7, str(self.floornum), shape="ellipse")
        new_rect = pygame.Rect(self.posx + self.width - 30, self.posy, 30, 20)
        self.transparent_surface = ImageFactory.create_transparent_surface(new_rect.width, new_rect.height, 128)
        self.transparent_surface_rect = self.transparent_surface.get_rect(topleft=new_rect.topleft)
        self.black_strip_rect = ImageFactory.create_rect(self.posx, self.posy + self.height - 3, self.width, 3)

    def draw(self):
        self.screen.blit(self.bricktexture, self.rect)
        self.button.draw()
        pygame.draw.rect(self.screen, (0, 0, 0), self.black_strip_rect)
        self.screen.blit(self.transparent_surface, self.transparent_surface_rect.topleft)
        self.button.draw()
        pygame.draw.rect(self.screen, (0, 0, 0), self.black_strip_rect)
        self.screen.blit(self.transparent_surface, self.transparent_surface_rect.topleft)
        a888 = (self.timewait) * 10
        a888 = int(a888)
        a888 /= 10
        font = pygame.font.Font(None, 25)
        font = pygame.font.Font(None, 25)
        number_text = font.render(str(a888), True, (139, 139, 0))
        number_text_rect = number_text.get_rect(center=self.transparent_surface_rect.center)
        number_text_rect = number_text.get_rect(center=self.transparent_surface_rect.center)
        self.screen.blit(number_text, number_text_rect)

    def checkclick(self, position):
        if self.button.checkclick(position) :
            if self.call_elevator():
              self.button.off_on()
    def call_elevator(self):
        if self.building.update(self):
            return True

    def finish(self):
        self.button.off_on()