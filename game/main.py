from button import *
from TextBox import *
import pygame
from Building import building

class ElevatorManagement:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.screen_width = info.current_w - 50
        self.screen_height = info.current_h - 100
        self.floor_width = 200
        self.rest1=0
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Building Simulation')
        self.clock = pygame.time.Clock()
        width_box = 140
        self.elevator_textbox = TextBox(self.screen_width * 0.3, 10, width_box, 32, '5')
        self.floor_textbox = TextBox(self.screen_width * 0.3 + width_box + 20, 10, width_box, 32, '17')
        self.building_textbox = TextBox(self.screen_width * 0.3 + (width_box + 20) * 2, 10, width_box, 32, '1')
        self.textboxes = [self.elevator_textbox, self.floor_textbox, self.building_textbox]

        self.start_button = ButtonFactory.create_button(self.screen, self.screen_width - 180, 30, 150, 50, "Start", "rect")

        self.running = True
        self.reset_simulation = False
        self.buildings = []
        self.simulation_started = False

    def create_buildings(self):
        try:
            num_elevators = int(self.elevator_textbox.text)
            num_floors = int(self.floor_textbox.text)
            num_buildings = int(self.building_textbox.text)
        except ValueError:
            num_elevators, num_floors, num_buildings = 5, 25, 1
        if self.screen_height / num_floors>110:
            self.screen = pygame.display.set_mode((self.screen_width, 110*num_floors))
            self.screen_height=110*num_floors                                     
        floor_height = self.screen_height / num_floors
        
        buildings = []
        for i in range(num_buildings):
            buildings.append(building(self.screen, floor_height, self.floor_width, num_elevators, 1, num_floors, (self.floor_width // 2 + num_elevators * 80 + 40) * i))

        self.buildings = buildings
        if self.rest1==0:
            self.start_button.text="rest"
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button.checkclick(event.pos):
                        self.reset_simulation = True
                    if self.simulation_started:
                        for bld in self.buildings:
                            for floor in bld.floors:
                                floor.checkclick(event.pos)
                
                if not self.simulation_started:
                    for textbox in self.textboxes:
                        textbox.handle_event(event)

            if self.reset_simulation:
                self.create_buildings()
                self.start_button.off_on()
                self.reset_simulation = False
                self.simulation_started = True
            
            self.screen.fill((255, 255, 255))
            for bld in self.buildings:
                bld.draw()
                bld.update1()
            self.start_button.draw()
            if not self.simulation_started:
                for textbox in self.textboxes:
                    textbox.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


class ElevatorManagementFactory:
    @staticmethod
    def create_elevator_management():
        return ElevatorManagement()


run1 = ElevatorManagementFactory.create_elevator_management()
run1.run()
