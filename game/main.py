
import pygame
from Building import building

def run_game():
    pygame.init()
    info = pygame.display.Info()
    screen_height = info.current_w  -50
    screen_width = info.current_h -50
    print(screen_width)  
    floor_height, floor_width, num_elevators,numfloors=  70, 200, 5,25
    num_bul=3
    
    screen = pygame.display.set_mode((screen_height, screen_width))
    pygame.display.set_caption('Building Simulation')
    clock = pygame.time.Clock()
    print(screen_width/numfloors)
    building_instance = building(screen, screen_width/numfloors, floor_width, num_elevators,1,numfloors)
    building_instance1 = building(screen, screen_width/numfloors, floor_width, num_elevators,1,numfloors,floor_width//2+num_elevators*80+40)
    a=1
    b=[]
    for i in range(0,num_bul):
     b.append(building(screen, screen_width/numfloors, floor_width, num_elevators,1,numfloors,(floor_width//2+num_elevators*80+40)*i))
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
                    for i in b:
                        for floor in i.floors:
                            floor.checkclick(event.pos)
                  
        screen.fill((255, 255, 255))  
        for i in b:
            i.draw()
            i.update1(dt)

      
        pygame.display.flip()  
        clock.tick(60)  

    pygame.quit()


run_game()