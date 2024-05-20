import pygame
from User_Interface_Components.ImageFactory import ImageFactory

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type, **kwargs):
        if shape_type == 'rectangle' or shape_type == 'rect':
            return ImageFactory.create_rectangle_surface(kwargs['width'], kwargs['height'], kwargs['color'])
        elif shape_type == 'transparent_surface':
            return ImageFactory.create_transparent_surface(kwargs['width'], kwargs['height'], kwargs['alpha'])
        elif shape_type == 'ellipse':
            return ImageFactory.create_ellipse_surface(kwargs['width'], kwargs['height'], kwargs['color'])
        elif shape_type == 'image':
            return ImageFactory.create_image(kwargs['image_path'], kwargs['width'], kwargs['height'])
        else:
            raise ValueError(f"Shape type '{shape_type}' is not supported.")
