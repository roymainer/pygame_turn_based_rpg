"""
Animator Class
Works with single sprite sheet and an atlas file

Created: Jul 30, 2018
@author: rmainer
"""
import pygame


def prepare_animations(spritesheet_file, atlas_file, sprite_size=None):

    sprite_sheet = pygame.image.load(spritesheet_file).convert_alpha()

    if atlas_file is None:
        atlas_file = spritesheet_file.replace("png", "txt")

    with open(atlas_file, "r") as f:
        lines = f.readlines()  # read entire file

    animation_dictionary = {}

    for line in lines:
        # Line example: air-attack1-00 = 0 38 50 37
        action_key, rect_vals = line.split(" = ")  # (air-attack1-00, 0 38 50 37)
        action = action_key.split("-")[:-1]  # [air, attack1]

        if len(action) > 1:
            action = "-".join(action)  # air-attack1
        else:
            action = action[0]  # action is list...

        if action not in animation_dictionary.keys():
            animation_dictionary[action] = []  # create a new list of sprites

        r = pygame.Rect(tuple([int(s) for s in rect_vals.split(' ')]))  # create a rect for sprite in sheet
        sprite = sprite_sheet.subsurface(r)  # get sprite as subsurface

        if sprite_size is not None:
            sprite = pygame.transform.scale(sprite, sprite_size)

        animation_dictionary[action].append(sprite)  # add to list

    return animation_dictionary


class Animator(object):

    def __init__(self, spritesheet_file, atlas_file=None, sprite_size=None):
        self.__animation_dict = prepare_animations(spritesheet_file, atlas_file, sprite_size)
        self.__animation_key = ""   # animation key (name)
        self.__sprite_index = 0     # index of current sprite in animation list of sprites
        self.__flip = False  # flip the image

    def get_animations_keys(self) -> []:
        return list(self.__animation_dict.keys())

    def get_animation_key(self):
        return self.__animation_key

    def get_sprite_index(self):
        return self.__sprite_index

    def get_next_sprite_index(self):

        if self.__animation_key == "":
            return 0

        index = self.get_sprite_index()
        if index == len(self.__animation_dict[self.__animation_key])-1:
            return 0
        else:
            return index + 1

    def set_flip(self):
        self.__flip = True

    def unset_flip(self):
        self.__flip = False

    def flip_sprites_ver(self):
        """
        Flips the x axis of the sprites in the animation dict
        """
        for action_key, sprites_list in self.__animation_dict.items():
            for i in range(0, len(sprites_list)):
                sprite = sprites_list[i]
                self.__animation_dict[action_key][i] = pygame.transform.flip(sprite, True, False)
        return self.__animation_dict

    def get_next_sprite(self, animation_key: str) -> pygame.Surface:
        """
        Returns the next sprite in the animation
        :param animation_key:
        :return: surface
        """

        if animation_key != self.__animation_key:
            # if changed to new animation, update key and reset sprite index
            self.__animation_key = animation_key
            self.__sprite_index = 0
        else:
            self.__sprite_index += 1
            if self.__sprite_index == len(self.__animation_dict[self.__animation_key]):
                self.__sprite_index = 0

        image = self.__animation_dict[self.__animation_key][self.__sprite_index]

        if self.__flip:
            image = pygame.transform.flip(image, True, False)

        return image

    def get_last_sprite(self) -> pygame.Surface:
        """
        Returns the last sprite in sprite list
        For example, if character died
        :return: surface
        """
        return self.__animation_dict[self.__animation_key][-1]

    def reset_animation(self):
        self.__sprite_index = 0


if __name__ == "__main__":
    import os

    SCREEN_SIZE = (480, 320)
    FPS = 60
    BLACK = (0, 0, 0)
    SPRITE_SHEET = os.path.join("..", "Assets", "adventurer_sprite_sheet.png")
    ATLAS = os.path.join("..", "Assets", "adventurer_sprite_sheet.txt")
    SIZE = (200, 148)
    ACTION = "bow"
    INTERVAL = .10  # how long one single sprite should be displayed in seconds

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    playtime = 0
    cycletime = 0

    animator = Animator(SPRITE_SHEET, ATLAS, sprite_size=SIZE)

    while 1:
        milliseconds = clock.tick(FPS)  # ms passed since last tick/frame
        seconds = milliseconds / 1000.0  # seconds since last tick/frame
        playtime += seconds
        cycletime += seconds
        if cycletime > INTERVAL:
            image = animator.get_next_sprite(ACTION)
            size = image.get_rect().size
            screen.fill(BLACK)
            screen.blit(image, (SCREEN_SIZE[0]/2 - size[0]/2, SCREEN_SIZE[1]/2 - size[1]/2))
            cycletime = 0

        pygame.display.set_caption("[FPS]: %.2f picture: %i" % (clock.get_fps(), animator.get_sprite_index()))
        pygame.display.flip()
