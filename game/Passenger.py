import pygame
import random
imgpassenger = "men1.png"

class Passenger:
    def __init__(self, current_floor):
        self.current_floor = current_floor
        self.destination = self.pick_random_destination()
        original_image = pygame.image.load(imgpassenger).convert_alpha()
        
        new_width = 20  # Example width
        new_height = 40  # Example height
        
        self.image = pygame.transform.smoothscale(original_image, (new_width, new_height))

    def pick_random_destination(self):
        # potential_destinations = list(range(Building.num_floors))
        # potential_destinations=5
        # potential_destinations.remove(self.current_floor)
        return random.randint(1, 5)

