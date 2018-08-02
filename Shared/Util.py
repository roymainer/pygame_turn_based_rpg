import pygame
from pygame import Surface
from pygame.rect import Rect
from pygame.sprite import Sprite
from Shared.Character import Character
from Shared.GameConstants import GameConstants
from Shared.GameObject import GameObject


def load_character(game_engine, scene, key, position, type):
    key = key.lower()
    sprite_sheet = Util.GAME_OBJECTS_DICT[key]["sprite_sheet"]
    size = Util.GAME_OBJECTS_DICT[key]["size"]
    new_position = (position[0] - size[0] / 2, position[1] - size[1] / 2)

    character = Character(sprite_sheet, size, new_position, type)  # init adventurer

    scene.add_game_object(character)  # add to scene objects list

    game_engine.add_sprite_to_group(character, type)  # add to game engine sprites group
    return


class Util:

    GAME_OBJECTS_DICT = {
        "adventurer":
            {"sprite_sheet": GameConstants.ADVENTURER_SPRITE_SHEET,
             "size": GameConstants.ADVENTURER_SIZE},
        "slime":
            {"sprite_sheet": GameConstants.SLIME_SPRITE_SHEET,
             "size": GameConstants.SLIME_SIZE}
    }


class Pointer(Sprite):
    """Pointer is used to detect which Sprite the mouse points at """

    def __init__(self, point):
        size = (1, 1)
        self.image = Surface(size)  # single pixel surface
        self.rect = Rect(point, size)
        super(Pointer, self).__init__()


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
