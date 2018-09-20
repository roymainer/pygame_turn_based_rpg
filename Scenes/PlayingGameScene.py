import pygame
from Managers.ActionManager import ActionManager
from Managers.EventsManager import EventsManager
from Managers.LevelManager import LevelManager
from Managers.MagicManager import MagicManager
from Managers.ModelsManager import ModelsManager
from Managers.PhaseManager import PhaseManager
from Managers.TurnManager import TurnManager
from Managers.UIManager import UIManager
from Shared.GameConstants import GameConstants
from Scenes.Scene import Scene
import logging
logger = logging.getLogger().getChild(__name__)


class PlayingGameScene(Scene):

    def __init__(self, game_engine):
        super(PlayingGameScene, self).__init__(game_engine)
        logger.info("Initiate managers:")
        self.__level_manager = LevelManager(self)  # level manager loads the level and models
        self.__phase_manager = PhaseManager(self)  # Phase manager handles turn phases (Magic/Shooting/Close Combat)
        self.__models_manager = ModelsManager(self)  # models manager handles the scenes models
        self.__turn_manager = TurnManager(self)  # handles the Turn (Phases and models turns)
        self.__action_manager = ActionManager(self)  # action manager handles each models action
        self.__ui_manager = UIManager(self)  # UI manager handles the battle menus
        self.__magic_manager = MagicManager(self)  # Magic manager handles the power pool during Magic Phase
        self.__events_manager = EventsManager(self)  # handles events and keyboard presses

        # initialize:
        self.__level_manager.load_level()  # load the level (will populate the models manager)
        self.__phase_manager.on_init()  # load the first battle phase (Magic Phase)

        self.create_background()  # TODO : move to load level

        # synchronization lock
        self.__lock = None

    def handle_events(self):
        self.__events_manager.handle_events()

    def update(self):

        self.draw_special_rules_of_focused_module()

        self.__turn_manager.update()
        self.__phase_manager.update()

    def draw_special_rules_of_focused_module(self):
        game_engine = self.get_game_engine()
        """ Remove any previously drawn special rule """
        for model in self.__models_manager.get_all_models_sorted_list():
            model.clear_special_rules_texts()

        """ Draw special rules of focused-on unit """
        for model in self.__models_manager.get_all_models_sorted_list():
            if model.collide_point(pygame.mouse.get_pos()):
                print("Collision with model: {} at: {}".format(model.get_name(), pygame.mouse.get_pos()))
                model.special_rules_to_texts()
                special_rules_texts = model.get_special_rules_texts()
                for srt in special_rules_texts:
                    game_engine.add_sprite_to_group(srt)
                break

    def get_action_manager(self) -> ActionManager:
        return self.__action_manager

    def get_level_manager(self) -> LevelManager:
        return self.__level_manager

    def get_models_manager(self) -> ModelsManager:
        return self.__models_manager

    def get_phase_manager(self) -> PhaseManager:
        return self.__phase_manager

    def get_turn_manager(self) -> TurnManager:
        return self.__turn_manager

    def get_ui_manager(self) -> UIManager:
        return self.__ui_manager

    def get_magic_manager(self) -> MagicManager:
        return self.__magic_manager

    def get_events_manager(self) -> EventsManager:
        return self.__events_manager

    def acquire_lock(self, locker: str) -> bool:
        if self.__lock is not None:
            if self.__lock == locker:
                return True
            else:
                return False

        else:
            # if lock is None, acquire the lock
            self.__lock = locker
            logger.info("{} ------ acquired the lock".format(locker))
            return True

    def release_lock(self, locker: str) -> bool:
        if self.__lock is not None:
            if self.__lock == locker:
                self.__lock = None
                logger.info("{} ------ released the lock".format(locker))
                return True
            else:
                # if manager doesn't have the right key, don't release and return False
                return False

        else:
            # if lock is None, nothing to release
            return True

    def create_background(self):
        # TODO: move to Level Manager
        surface = pygame.Surface(GameConstants.SCREEN_SIZE)  # create an empty surface

        # load upper background
        background = pygame.image.load(GameConstants.DARK_LAIR)
        background = pygame.transform.smoothscale(background, (GameConstants.SCREEN_SIZE[0],
                                                               GameConstants.BATTLE_AREA_TOP))
        surface.blit(background, (0, 0))

        battleground_tile = pygame.image.load(GameConstants.CAVE_TILE)
        rows = 2
        columns = 8
        tile_width = int(GameConstants.SCREEN_SIZE[0] / columns)  # 800 / 8 = 100
        tile_height = int((GameConstants.BATTLE_AREA_BOTTOM - GameConstants.BATTLE_AREA_TOP) / rows)  # 200/ 2 = 100

        battleground_tile = pygame.transform.scale(battleground_tile,
                                                   (tile_width, tile_height))

        y = GameConstants.BATTLE_AREA_TOP
        for row in range(rows):
            y += tile_height * row
            for column in range(columns):
                x = tile_width * column
                surface.blit(battleground_tile, (x, y))

        self.get_game_engine().set_background(surface)
        return
