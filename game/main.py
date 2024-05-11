from button import *

import pygame
from Building import building

def run_game():
    pygame.init()
    info = pygame.display.Info()
    screen_height = info.current_w  -50
    screen_width = info.current_h -100
      
    floor_height, floor_width, num_elevators,numfloors=  70, 200, 5,25
    num_bul=3
    
    screen = pygame.display.set_mode((screen_height, screen_width))
    pygame.display.set_caption('Building Simulation')
    clock = pygame.time.Clock()
    initbul=ButtonFactory.create_button(screen, screen_height-80, 30, 100, 50, "Start", "rect")
    
    b=[]
    for i in range(0,num_bul):
     b.append(building(screen, screen_width/numfloors, floor_width, num_elevators,1,numfloors,(floor_width//2+num_elevators*80+40)*i))
    running = True
    a111=0
    while running:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                  
                if event.button == 1:  
                    a111=initbul.checkclick(event.pos)
                    for i in b:
                        # a12=i.elevators[0].setfloor(event.pos[1])#לשים לב שיש כאן הנחה שקיים
                        # i.locatefloor[a12].checkclick(event.pos)
                        for floor in i.floors:
                            
                            floor.checkclick(event.pos)
        if a111:
            print(22)
            for i in b:
             for i1 in i.elevators:
                i.restelv()    
        a111=0
        screen.fill((255, 255, 255))  
        for i in b:
            i.draw()
            i.update1()
        initbul.draw()
      
        pygame.display.flip()  
        clock.tick(60)  

    pygame.quit()


run_game()