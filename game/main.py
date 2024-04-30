
import pygame
from Building import building

def run_game():
    screen_width, screen_height, floor_height, floor_width, num_elevators,numfloors=1000, 1800, 70, 200, 5,25
    pygame.init()
    screen = pygame.display.set_mode((1800, 1000))
    pygame.display.set_caption('Building Simulation')
    clock = pygame.time.Clock()
    print(screen_width/numfloors)
    # building_instance = building(screen, screen_width/numfloors, floor_width, num_elevators)
    building_instance = building(screen, screen_width/numfloors, floor_width, num_elevators,1,numfloors)

    a=1
    running = True
    while running:
        if a==1:
         dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse Clicked at:", event.pos)  
                if event.button == 1:  
                    for floor in building_instance.floors:
                        floor.checkclick(event.pos)

        screen.fill((255, 255, 255))  
        building_instance.draw()  
        building_instance.update1(dt)
        pygame.display.flip()  
        clock.tick(60)  

    pygame.quit()


run_game()