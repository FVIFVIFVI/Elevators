import pygame
from User_Interface_Components.TextBox import TextBox
from factory.ButtonFactory import ButtonFactory

class ErrorMessage:
    """A drawable error message object."""
    def __init__(self, text, font, color, center_pos):
        self.font = font
        self.color = color
        self.center_pos = center_pos
        self.surface = self.font.render(text, True, self.color)
        self.rect = self.surface.get_rect(center=self.center_pos)

    def draw(self, screen):
        """Draws the error message onto the provided screen."""
        screen.blit(self.surface, self.rect)


class InitialSetupScreen:
    """
    Represents the initial setup screen, using a list of drawable components.
    """
    def __init__(self, target_main_sim_width, target_main_sim_height, config_floor_width, building_layout_class):
        """
        Initializes the Pygame window and UI components.

        Args:
            target_main_sim_width (int): The target width for the main simulation window.
            target_main_sim_height (int): The target height for the main simulation window.
            config_floor_width (int): The configured width of a floor in the simulation.
            building_layout_class: The class responsible for validating the building layout.
        """
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
        self.error_message_color = (255, 0, 0)
        
        # --- Component Creation ---
        width_box = 200
        start_x_textboxes = (self.screen_width - (3 * width_box + 2 * 20)) // 2
        self.elevator_textbox = TextBox(start_x_textboxes, 50, width_box, 32, 'Elevators')
        self.floor_textbox = TextBox(start_x_textboxes + width_box + 20, 50, width_box, 32, 'Floors')
        self.building_textbox = TextBox(start_x_textboxes + (width_box + 20) * 2, 50, width_box, 32, 'Buildings')
        
        button_width = 200
        button_height = 50
        button_x = (self.screen_width - button_width) // 2
        button_y = 120
        self.confirm_button = ButtonFactory.create_button(self.screen, button_x, button_y, button_width, button_height, "Confirm Settings", "rect")

        # Central list of all objects to be drawn
        self.drawable_components = [self.elevator_textbox, self.floor_textbox, self.building_textbox, self.confirm_button]
        self.error_message_object = None
        
        self.running = True

    def _update_error_message(self, message):
        """
        Manages the error message object by adding or removing it from the drawable list.
        
        Args:
            message (str or None): The text of the error to display, or None to clear it.
        """
        if self.error_message_object in self.drawable_components:
            self.drawable_components.remove(self.error_message_object)
            self.error_message_object = None

        if message:
            center_pos = (self.screen_width // 2, 190)
            self.error_message_object = ErrorMessage(message, self.font, self.error_message_color, center_pos)
            self.drawable_components.append(self.error_message_object)

    def get_simulation_parameters(self):
        """
        Runs the main event loop, handles input, and validates parameters.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None

                for textbox in [self.elevator_textbox, self.floor_textbox, self.building_textbox]:
                    textbox.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.confirm_button.checkclick(event.pos):
                        num_elevators, num_floors, num_buildings_requested = 0, 0, 0
                        
                        try:
                            num_elevators_str = self.elevator_textbox.text
                            num_floors_str = self.floor_textbox.text
                            num_buildings_requested_str = self.building_textbox.text

                            num_elevators = int(num_elevators_str) if num_elevators_str else 0
                            num_floors = int(num_floors_str) if num_floors_str else 0
                            num_buildings_requested = int(num_buildings_requested_str) if num_buildings_requested_str else 0

                            if num_elevators <= 0 or num_floors <= 0 or num_buildings_requested <= 0:
                                raise ValueError("Inputs must be positive integers.")
                            
                            self._update_error_message(None) # Clear previous errors if input is valid so far

                        except ValueError as e:
                            self._update_error_message(f"Invalid input: {e}. Using defaults: 5 elevators, 25 floors, 2 buildings.")
                            num_elevators, num_floors, num_buildings_requested = 5, 25, 2
                            self.elevator_textbox.text = str(num_elevators)
                            self.floor_textbox.text = str(num_floors)
                            self.building_textbox.text = str(num_buildings_requested)
                            continue

                        layout_validator = self.building_layout_class(
                            initial_screen_h=self.target_main_sim_height,
                            num_floors_val=num_floors,
                            num_elevators_val=num_elevators,
                            num_buildings_requested=num_buildings_requested,
                            config_floor_width=self.config_floor_width,
                            screen_width_param=self.target_main_sim_width
                        )
                        actual_num_buildings = layout_validator.num_buildings

                        if layout_validator.bound_bulding:
                            self._update_error_message(layout_validator.bound_bulding["error"])
                            continue

                        if actual_num_buildings == 0 and num_buildings_requested > 0:
                            self._update_error_message("Error: No buildings fit. Check settings.")
                            continue
                        elif actual_num_buildings < num_buildings_requested:
                            self._update_error_message(f"Warning: Only {actual_num_buildings} of {num_buildings_requested} fit. Using {actual_num_buildings}.")
                        
                        # Proceed if there are no blocking errors
                        if not (self.error_message_object and "Error:" in self.error_message_object.surface.get_colorkey()): # A simple way to check if the current message is a blocking error
                             final_floor_height = layout_validator.get_floor_height()
                             final_screen_height = layout_validator.get_final_building_height()
                             building_start_x_coords = [boundary['x1'] for boundary in layout_validator.building_boundaries]

                             if final_floor_height <= 0 and num_floors > 0:
                                 self._update_error_message("Error: Calculated floor height is zero or less.")
                                 continue
                             else:
                                 self.running = False
                                 pygame.display.quit()
                                 return (num_elevators, num_floors, actual_num_buildings,
                                         final_floor_height, final_screen_height, building_start_x_coords)

            # --- Drawing Section ---
            self.screen.fill((220, 220, 220))
            
            # Single loop to draw all components
            for component in self.drawable_components:
                try:
                    component.draw(self.screen)
                except TypeError:
                    component.draw()

            pygame.display.flip()

        pygame.display.quit()
        return None