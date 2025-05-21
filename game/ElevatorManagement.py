import pygame
from factory.ButtonFactory import ButtonFactory
from factory.buildingfactory import BuildingFactory
from SetupScreen import InitialSetupScreen

# --- ייבוא BuildingLayout ---
# שנה את השורה הבאה כדי לייבא את BuildingLayout מהמיקום הנכון בפרויקט שלך
# לדוגמה: from building_layout_module import BuildingLayout
# או אם BuildingLayout מוגדר בקובץ שנגיש ישירות:
# from BuildingLayout import BuildingLayout # אם זה שם הקובץ והקלאס
# אם BuildingLayout מוגדר באותו קובץ כמו ElevatorManagement (פחות סביר בהינתן ההפרדה לקבצים), אין צורך בייבוא.
# לצורך הדגמה, אניח שיש קובץ building_layout.py שממנו ניתן לייבא.
# **הערה חשובה:** החלף את השורה הבאה בייבוא הנכון שלך!
from BuildingLayout import BuildingLayout # <--- שנה ייבוא זה בהתאם למבנה הפרויקט שלך

class ElevatorManagement:
    def __init__(self): # החתימה חזרה למקורית, ללא פרמטרים
        self.screen = None
        self.screen_width = 0
        self.screen_height = 0
        
        self.floor_width = 200
        # ElevatorManagement ישתמש ישירות בקלאס BuildingLayout המיובא
        self.building_layout_class_ref = BuildingLayout 

        self.clock = None
        self.buildings = []
        self.running = True
        self.simulation_started = False
        self.needs_reconfiguration = True

        self.num_elevators = 0
        self.num_floors = 0
        self.actual_num_buildings = 0
        self.calculated_floor_height = 0
        self.building_start_x_coords = []
        
        self.reconfigure_button = None

    def perform_initial_setup(self):
        pygame.init()
        info = pygame.display.Info()
        target_screen_width = info.current_w - 50
        target_screen_height = info.current_h - 100

        setup_screen = InitialSetupScreen(
            target_screen_width, 
            target_screen_height, 
            self.floor_width,
            self.building_layout_class_ref # מעביר את הקלאס BuildingLayout שייבאנו
        )
        params = setup_screen.get_simulation_parameters()

        if params is None:
            self.running = False
            return False

        (self.num_elevators, self.num_floors, self.actual_num_buildings,
         self.calculated_floor_height, adjusted_main_screen_height, self.building_start_x_coords) = params

        self.screen_width = target_screen_width
        self.screen_height = adjusted_main_screen_height

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Building Simulation')
        self.clock = pygame.time.Clock()

        if self.screen:
             self.reconfigure_button = ButtonFactory.create_button(
                 self.screen, self.screen_width - 180, 10, 150, 40,
                 "Reconfigure", "rect"
             )
        return True

    def create_buildings_from_params(self):
        self.buildings = []
        if self.actual_num_buildings == 0:
            return

        if self.calculated_floor_height <= 0 and self.num_floors > 0:
             return

        for i in range(self.actual_num_buildings):
            start_x = self.building_start_x_coords[i]
            building = BuildingFactory.create_building(
                self.screen,
                self.calculated_floor_height,
                self.floor_width,
                self.num_elevators,
                1, 
                self.num_floors,
                start_x
            )
            self.buildings.append(building)
        
        self.simulation_started = True

    def run(self):
        while self.running:
            if self.needs_reconfiguration:
                setup_successful = self.perform_initial_setup()
                if not setup_successful:
                    if not self.running:
                        break 
                
                if self.screen:
                    self.create_buildings_from_params()
                    self.needs_reconfiguration = False
                else:
                    self.running = False 
                    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                clicked_on_button = False
                if self.screen and self.reconfigure_button and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.reconfigure_button.checkclick(event.pos):
                        self.needs_reconfiguration = True
                        clicked_on_button = True
                
                if self.simulation_started and not self.needs_reconfiguration and not clicked_on_button:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for bld in self.buildings:
                            if hasattr(bld, 'floors'):
                                for floor in bld.floors:
                                    if hasattr(floor, 'checkclick'):
                                        floor.checkclick(event.pos)
            
            if not self.running:
                break

            if self.screen and not self.needs_reconfiguration:
                self.screen.fill((255, 255, 255))
                for bld in self.buildings:
                    if hasattr(bld, 'draw'): bld.draw()
                    if hasattr(bld, 'update'): bld.update()
                
                if self.reconfigure_button:
                    self.reconfigure_button.draw()
                
                pygame.display.flip()
                if self.clock:
                    self.clock.tick(60)
            elif self.needs_reconfiguration and self.running:
                pass

        pygame.quit()


class ElevatorManagementFactory:
    @staticmethod
    def create_elevator_management(): # החתימה חזרה למקורית, ללא פרמטרים
        return ElevatorManagement()