import pygame

from Shared.Animator import Animator
from Shared.Bestiary import *
from Shared.GameConstants import GameConstants


class Act:

    def __init__(self, level, sprite_sheet):
        self.__animator = Animator(spritesheet_file=sprite_sheet,
                                   atlas_file=None,
                                   sprite_size=GameConstants.SCREEN_SIZE)
        self.__level = level

    def get_image_by_key(self, key):
        if key not in self.__animator.get_animations_keys():
            key = self.__animator.get_animations_keys()[0]
        return self.__animator.get_sprite_by_key(key)

    def get_campaign_background(self):
        pass

    def get_level(self):
        return self.__level

    def get_level_key(self):
        return "level"+self.__level


class Act1(Act):

    def __init__(self, level):
        super(Act1, self).__init__(level, GameConstants.ACT1_PATH_SPRITE_SHEET)

    def get_campaign_background(self):
        background = pygame.image.load(GameConstants.ACT1_BACKGROUND)
        background = pygame.transform.smoothscale(background, GameConstants.SCREEN_SIZE)

        level_key = self.get_level_key()
        level_image = self.get_image_by_key(level_key)
        level_rect = level_image.get_rect()

        background.blit(level_image, (level_rect.left, level_rect.top))  # blit paths over background map

        return background

    def get_next_round_models(self) -> dict:

        if self.get_level() == '1':
            # TODO: this should be loaded from an xml
            player_models_dict = {GameConstants.PLAYER_MIDDLE_FRONT: get_dwarf_hero}
            computer_models_dict = {GameConstants.COMPUTER_TOP_FRONT: get_skaven_slave,
                                    GameConstants.COMPUTER_MIDDLE_FRONT: get_skaven_slave,
                                    GameConstants.COMPUTER_BOTTOM_FRONT: get_skaven_slave}

            return {GameConstants.PLAYER_OBJECT: player_models_dict,
                    GameConstants.COMPUTER_OBJECT: computer_models_dict}


# acts dict returns the act matching the level number (many to one)
LEVELS_TO_ACTS_DICT = {"1": Act1, "2": Act1, "3": Act1, "4": Act1, "5": Act1, "6": Act1, "7": Act1, "8": Act1}


def get_act_object(level):
    return LEVELS_TO_ACTS_DICT[level]
