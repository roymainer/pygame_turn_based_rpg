import pygame
from Managers.ActionManager import ActionManager
from Managers.LevelManager import LevelManager
from Managers.ModelsManager import ModelsManager
from Managers.PhaseManager import PhaseManager
from Managers.TurnManager import TurnManager
from Managers.UIManager import UIManager
from Shared.GameConstants import *
from Scenes.Scene import Scene


class PlayingGameScene(Scene):

    def __init__(self, game_engine):
        super(PlayingGameScene, self).__init__(game_engine)

        self.__level_manager = LevelManager(self)  # level manager loads the level and models
        self.__phase_manager = PhaseManager(self)
        self.__models_manager = ModelsManager()  # models manager handles the scenes models
        self.__turn_manager = TurnManager(self)  # handles the Turn (Phases and models turns)
        self.__action_manager = ActionManager(self)  # action manager handles each models action
        self.__ui_manager = UIManager(self)  # UI manager handles the battle menus

        self.__level_manager.load_level()  # load the level (will populate the models manager)
        self.__phase_manager.set_next_phase()  # load the first battle phase (Magic Phase)
        self.__ui_manager.on_init()  # create player/computer menus

        self.create_background()  # TODO : move to load level

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:

                current_model = self.__turn_manager.get_current_model()
                if current_model.get_type() == COMPUTER_OBJECT:
                    return  # if not player turn, ignore key stroke

                if event.key == pygame.K_ESCAPE:
                    self.__ui_manager.return_to_previous_menu()
                if event.key == pygame.K_UP:
                    self.__ui_manager.move_pointer_up()
                    # need to add move computer marker up
                if event.key == pygame.K_DOWN:
                    self.__ui_manager.move_pointer_down()
                    # need to add move computer marker down
                if event.key == pygame.K_RETURN:
                    self.__ui_manager.menu_item_pressed()

    def update(self):

        self.__turn_manager.update()
        self.__phase_manager.update()

    def get_action_manager(self):
        return self.__action_manager

    # def get_current_model(self):
    #     return self.__turn_manager.get_current_model()

    def get_models_manager(self) -> ModelsManager:
        return self.__models_manager

    def get_phase_manager(self) -> PhaseManager:
        return self.__phase_manager

    def get_turn_manager(self) -> TurnManager:
        return self.__turn_manager

    def get_ui_manager(self) -> UIManager:
        return self.__ui_manager

    def create_background(self):
        # TODO: move to Level Manager
        surface = pygame.Surface(SCREEN_SIZE)  # create an empty surface

        # load upper background
        background = pygame.image.load(DARK_LAIR)
        background = pygame.transform.smoothscale(background, (SCREEN_SIZE[0],
                                                               BATTLE_AREA_TOP))
        surface.blit(background, (0, 0))

        battleground_tile = pygame.image.load(CAVE_TILE)
        rows = 2
        columns = 8
        tile_width = int(SCREEN_SIZE[0] / columns)  # 800 / 8 = 100
        tile_height = int((BATTLE_AREA_BOTTOM - BATTLE_AREA_TOP) / rows)  # 200/ 2 = 100

        battleground_tile = pygame.transform.scale(battleground_tile,
                                                   (tile_width, tile_height))

        y = BATTLE_AREA_TOP
        for row in range(rows):
            y += tile_height * row
            for column in range(columns):
                x = tile_width * column
                surface.blit(battleground_tile, (x, y))

        self.get_game_engine().set_background(surface)
        return
