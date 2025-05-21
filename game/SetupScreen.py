import pygame
from User_Interface_Components.TextBox import TextBox
from factory.ButtonFactory import ButtonFactory
# BuildingLayout יועבר כפרמטר לקונסטרקטור, כך שאין צורך לייבא אותו ישירות כאן.

class InitialSetupScreen:
    def __init__(self, target_main_sim_width, target_main_sim_height, config_floor_width, building_layout_class):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 250
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Initial Setup')

        self.target_main_sim_width = target_main_sim_width
        self.target_main_sim_height = target_main_sim_height
        self.config_floor_width = config_floor_width
        self.building_layout_class = building_layout_class

        self.font = pygame.font.Font(None, 32)
        self.error_message = None
        self.error_message_color = (255, 0, 0)

        width_box = 200
        start_x_textboxes = (self.screen_width - (3 * width_box + 2 * 20)) // 2
        
        self.elevator_textbox = TextBox(start_x_textboxes, 50, width_box, 32, 'Elevators')
        self.floor_textbox = TextBox(start_x_textboxes + width_box + 20, 50, width_box, 32, 'Floors')
        self.building_textbox = TextBox(start_x_textboxes + (width_box + 20) * 2, 50, width_box, 32, 'Buildings')
        self.textboxes = [self.elevator_textbox, self.floor_textbox, self.building_textbox]

        button_width = 200
        button_height = 50
        button_x = (self.screen_width - button_width) // 2
        button_y = 120
        self.confirm_button = ButtonFactory.create_button(self.screen, button_x, button_y, button_width, button_height, "Confirm Settings", "rect")
        
        self.running = True

    def get_simulation_parameters(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None

                for textbox in self.textboxes:
                    textbox.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.confirm_button.checkclick(event.pos):
                        try:
                            num_elevators_str = self.elevator_textbox.text
                            num_floors_str = self.floor_textbox.text
                            num_buildings_requested_str = self.building_textbox.text

                            num_elevators = int(num_elevators_str) if num_elevators_str else 0
                            num_floors = int(num_floors_str) if num_floors_str else 0
                            num_buildings_requested = int(num_buildings_requested_str) if num_buildings_requested_str else 0
                            
                            if num_elevators <= 0 or num_floors <= 0 or num_buildings_requested <= 0:
                                raise ValueError("Inputs must be positive integers.")

                        except ValueError:
                            num_elevators, num_floors, num_buildings_requested = 5, 25, 2
                            self.error_message = "Invalid input. Using defaults: 5 Elevators, 25 Floors, 2 Buildings."
                            self.elevator_textbox.text = str(num_elevators)
                            self.floor_textbox.text = str(num_floors)
                            self.building_textbox.text = str(num_buildings_requested)
                        
                        layout_validator = self.building_layout_class(
                            initial_screen_h=self.target_main_sim_height,
                            num_floors_val=num_floors,
                            num_elevators_val=num_elevators,
                            num_buildings_requested=num_buildings_requested,
                            config_floor_width=self.config_floor_width,
                            screen_width_param=self.target_main_sim_width
                        )

                        actual_num_buildings = layout_validator.num_buildings
                        
                        if actual_num_buildings == 0 and num_buildings_requested > 0:
                             self.error_message = f"Error: No buildings fit. Check settings."
                        elif actual_num_buildings < num_buildings_requested:
                            self.error_message = (f"Warning: Only {actual_num_buildings} of {num_buildings_requested} fit. Using {actual_num_buildings}.")
                        else:
                            self.error_message = None

                        if (actual_num_buildings > 0 or num_buildings_requested == 0) and \
                           not (self.error_message and "Error:" in self.error_message):
                            final_floor_height = layout_validator.get_floor_height()
                            final_screen_height = layout_validator.get_final_building_height()
                            
                            # --- !!! תיקון כאן !!! ---
                            # במקום לקרוא למתודה לא קיימת, ניגש ישירות ל- building_boundaries
                            # ונחלץ את הערכים של 'x1' מכל מילון ברשימה.
                            building_start_x_coords = [boundary['x1'] for boundary in layout_validator.building_boundaries]
                            # --- סוף התיקון ---

                            if final_floor_height <= 0 and num_floors > 0:
                                self.error_message = "Error: Calculated floor height is zero or less."
                            else:
                                self.running = False
                                pygame.display.quit() # סגירת חלון ההגדרות
                                return (num_elevators, num_floors, actual_num_buildings,
                                        final_floor_height, final_screen_height, building_start_x_coords)
            
            self.screen.fill((220, 220, 220))
            for textbox in self.textboxes:
                textbox.draw(self.screen)
            self.confirm_button.draw()

            if self.error_message:
                error_surface = self.font.render(self.error_message, True, self.error_message_color)
                error_rect = error_surface.get_rect(center=(self.screen_width // 2, 190))
                self.screen.blit(error_surface, error_rect)
            
            pygame.display.flip()

        pygame.display.quit() # למקרה שהלולאה הסתיימה מסיבה אחרת
        return None