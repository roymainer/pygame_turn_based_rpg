import pygame
from pygame import Surface
from pygame.rect import Rect
from pygame.sprite import Sprite
from Shared.GameConstants import GameConstants
from Shared.GameObject import GameObject


class MousePointer(Sprite):
    """Pointer is used to detect which Sprite the mouse points at """

    def __init__(self, point):
        size = (1, 1)
        self.image = Surface(size)  # single pixel surface
        self.rect = Rect(point, size)
        super(MousePointer, self).__init__()


class Marker(GameObject):
    """ Marks the selected game object """

    def __init__(self, rect):
        width = rect.width
        height = int(rect.height/4)
        left = rect.left
        top = rect.bottom - height/2
        new_rect = pygame.Rect((left, top), (width, height))  # create a new rect for the image

        image = Surface((new_rect.width, new_rect.height))  # create a new image surface
        pygame.draw.ellipse(image, GameConstants.BRIGHT_GREEN, rect, 1)  # draw the ellipse
        # image.fill(GameConstants.BRIGHT_GREEN)
        position = (new_rect.left, new_rect.top)  # get the position
        super(Marker, self).__init__(image, position)  # init the GameObject base class
