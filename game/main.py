from button import *
import pygame
from Building import building

def run_game():
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w - 50
    screen_width*=1
    screen_height = info.current_h - 100
    screen_height *=1
    floor_height, floor_width = 70, 200
    num_elevators, num_floors = 5, 25
    num_buildings = 1
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Building Simulation')
    clock = pygame.time.Clock()
    start_button = ButtonFactory.create_button(screen, screen_width - 80, 30, 100, 50, "rest", "rect")
    
    buildings = []
    for i in range(num_buildings):
        buildings.append(building(screen, screen_height / num_floors, floor_width, num_elevators, 1, num_floors, (floor_width // 2 + num_elevators * 80 + 40) * i))

    running = True
    rest_simulation = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.checkclick(event.pos):
                    rest_simulation = True
                for bld in buildings:
                    for floor in bld.floors:
                        floor.checkclick(event.pos)

        if rest_simulation:
            for bld in buildings:
                bld.reset_elevators()
                start_button.off_on()
            rest_simulation = False

        screen.fill((255, 255, 255))
        for bld in buildings:
            bld.draw()
            bld.update1()
        start_button.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

run_game()
