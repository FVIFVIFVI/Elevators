import pygame

class ImageFactory:
    @staticmethod
    def create_image(image_path, width, height):
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))

    @staticmethod
    def create_rectangle_surface(width, height, color):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect())
        return surface

    @staticmethod
    def create_rect(posx, posy, width, height):
        return pygame.Rect(posx, posy, width, height)

    @staticmethod
    def create_transparent_surface(width, height, alpha):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, alpha))
        return surface
