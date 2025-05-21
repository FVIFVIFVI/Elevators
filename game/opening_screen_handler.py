import pygame

class OpeningScreenHandler:
    def __init__(self, screen, clock, textboxes_list, start_button_obj):
        self.screen = screen
        self.clock = clock
        self.textboxes = textboxes_list
        self.start_button = start_button_obj
        self.elevator_textbox = self.textboxes[0]
        self.floor_textbox = self.textboxes[1]
        self.building_textbox = self.textboxes[2]

    def run_input_loop(self):
        input_screen_active = True
        start_pressed_on_this_screen = False

        while input_screen_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_screen_active = False
                    start_pressed_on_this_screen = False

                for textbox in self.textboxes:
                    textbox.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button.checkclick(event.pos):
                        start_pressed_on_this_screen = True
                        input_screen_active = False

            self.screen.fill((255, 255, 255))

            for textbox in self.textboxes:
                textbox.draw(self.screen)
            self.start_button.draw()

            pygame.display.flip()
            self.clock.tick(60)

        return start_pressed_on_this_screen