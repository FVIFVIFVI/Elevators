from factory.ImageFactory import *
from factory.ButtonFactory import *
import pygame

image_floor = 'game/images and sounds/floor.png'

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
        self.bricktexture = ImageFactory.create_image(image_floor, width, height)
        self.rect = self.bricktexture.get_rect(topleft=(posx, posy))
        posxb, posyb = posx + width - 80, posy + 10
        new_rect = pygame.Rect(self.posx + self.width - 30, self.posy, 30, 20)
        self.transparent_surface = ImageFactory.create_transparent_surface(new_rect.width, new_rect.height, 128)
        self.transparent_surface_rect = self.transparent_surface.get_rect(topleft=new_rect.topleft)
        self.black_strip_rect = ImageFactory.create_rect(self.posx, self.posy + self.height - 3, self.width, 3)

        button_width, button_height = width // 2, int(height * 0.7)
        free_width = width - new_rect.width - 2
        posxb = posx + (free_width - button_width)
        posyb = posy + (height - button_height) // 2
        self.button = ButtonFactory.create_button(screen, posxb, posyb, button_width, button_height, str(self.floornum), shape="ellipse")

    def draw(self):
        self.screen.blit(self.bricktexture, self.rect)
        self.button.draw()
        pygame.draw.rect(self.screen, (0, 0, 0), self.black_strip_rect)
        self.screen.blit(self.transparent_surface, self.transparent_surface_rect.topleft)
        rounded_wait_time = (self.timewait) * 10 # We want to round to the nearest tenth of a second
        rounded_wait_time = int(rounded_wait_time)
        rounded_wait_time /= 10
        font = pygame.font.Font(None, 25)
        number_text = font.render(str(rounded_wait_time), True, (139, 139, 0))
        number_text_rect = number_text.get_rect(center=self.transparent_surface_rect.center)
        self.screen.blit(number_text, number_text_rect)

    def checkclick(self, position):
        if self.button.checkclick(position):
            self.call_elevator()

    def call_elevator(self): # Receives the call from the keyboard through the main interface, updates the building, and gets an answer to light the button and in what color
        The_answer_from_the_building = self.building.choose_optimal_elevator(self)
        if The_answer_from_the_building == 1:
            self.button.off_on()
        if The_answer_from_the_building == 2:
            self.button.set_error()
    
    def finish(self):
        self.button.off_on()
