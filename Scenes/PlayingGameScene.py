import pygame

from Shared.Bestiary import *
from Scenes.Scene import Scene
from Shared.GameConstants import GameConstants
from TurnManager import TurnManager
from ActionManager import ActionManager
from UI.PlayingGameSceneUI import PlayingGameSceneUI


class PlayingGameScene(Scene):

    def __init__(self, game_engine):
        super(PlayingGameScene, self).__init__(game_engine)

        self.__turn_manager = TurnManager()  # 1st load the turn manager
        self.__action_manager = ActionManager(self.__turn_manager)  # 1.5 load the action manager
        self.load_level()  # 2nd load the level which will populate the turn manager with units
        self.__UI = PlayingGameSceneUI(self)  # 3rd, the UI will be created with units menus

        self.__current_model = None

        self.create_background()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:

                current_model = self.__turn_manager.get_current_model()
                if current_model.get_type() == GameConstants.COMPUTER_GAME_OBJECTS:
                    return  # if not player turn, ignore key stroke

                if event.key == pygame.K_ESCAPE:
                    self.__UI.return_to_previous_menu()
                if event.key == pygame.K_UP:
                    self.__UI.move_pointer_up()
                    # need to add move computer marker up
                if event.key == pygame.K_DOWN:
                    self.__UI.move_pointer_down()
                    # need to add move computer marker down
                if event.key == pygame.K_RETURN:
                    self.__UI.menu_item_pressed()

    def update(self):

        # focused_menu = self.__UI.get_focused_menu()
        # if focused_menu is not None:
        #     print("Focused Menu: {}".format(focused_menu.get_name()))

        current_model = self.__turn_manager.get_current_model()
        if current_model is not None:
            if current_model != self.__current_model:
                print("Current Unit's turn: {}".format(current_model.get_name()))
                self.__UI.update_models_menu()  # remove killed models from menus
                self.__current_model = current_model  # store the current model
                # self.__current_action = ActionManager(current_model)  # create a new action for the model
                self.__UI.add_player_marker(current_model)  # add a new marker for the model
                self.__UI.add_actions_menu(current_model)  # add new actions menu for the model

                """ Display Special Rules """
                for model in self.__turn_manager.get_all_models_list():
                    model.hide_models_special_rules()
                current_model.special_rules_to_texts()
                for text in current_model.get_texts():
                    game = self.get_game()
                    game.add_sprite_to_group(text, None, 0)

                if current_model in self.__turn_manager.get_all_computer_models():
                    # check if model is a computer model
                    self.play_computer_turn(current_model)

        """ Perform Action """
        # if self.__current_action.is_ready():
        if self.__action_manager.is_ready():
            # self.__current_action.perform_action()
            self.__action_manager.perform_action()
            # for text in self.__current_action.get_texts():
            for text in self.__action_manager.get_texts():
                self.get_game().add_sprite_to_group(text, None)

        """ Wait for animation to finish """
        # if self.__current_action.is_finished():
        if self.__action_manager.is_finished():

            """ Remove any dead units """
            for model in self.__turn_manager.get_all_models_list():
                if model.is_killed():
                    model.destroy(self.__turn_manager)  # TODO: I don't like passing TM as argument when a model is killed
                    self.__turn_manager.remove_model(model)

            # self.__current_unit.set_action("idle")  # return acting model to idle
            # self.__current_action.reset_action()
            # self.__current_action = None  # remove the current action
            self.__action_manager.reset_action()
            self.__current_model = None  # remove the current model
            self.__turn_manager.advance_to_next_model()  # advance the turn manager to next model

    def get_action_manager(self):
        return self.__action_manager

    def get_current_model(self):
        return self.__current_model

    def get_turn_manager(self):
        return self.__turn_manager

    def load_level(self):
        # load adventurer
        object_type = GameConstants.PLAYER_GAME_OBJECTS
        # self.load_model(get_empire_archer(), GameConstants.PLAYER_TOP_BACK, object_type)
        # self.load_model(get_empire_archer(), GameConstants.PLAYER_MIDDLE_BACK, object_type)
        # self.load_model(get_empire_archer(), GameConstants.PLAYER_BOTTOM_BACK, object_type)  # maintain this order
        # self.load_model(get_empire_swordsman(), GameConstants.PLAYER_TOP_FRONT, object_type, flip_x=True)
        # self.load_model(get_empire_swordsman(), GameConstants.PLAYER_MIDDLE_FRONT, object_type, flip_x=True)
        # self.load_model(get_empire_swordsman(), GameConstants.PLAYER_BOTTOM_FRONT, object_type, flip_x=True)

        self.load_model(get_empire_witch_hunter(), GameConstants.PLAYER_TOP_FRONT, object_type)
        self.load_model(get_warrior_priest(), GameConstants.PLAYER_MIDDLE_FRONT, object_type)
        self.load_model(get_empire_witch_hunter(), GameConstants.PLAYER_BOTTOM_FRONT, object_type)

        object_type = GameConstants.COMPUTER_GAME_OBJECTS
        # self.load_model(get_slime_monster(), GameConstants.COMPUTER_TOP_BACK, object_type)
        # self.load_model(get_slime_monster(), GameConstants.COMPUTER_MIDDLE_BACK, object_type)
        # self.load_model(get_slime_monster(), GameConstants.COMPUTER_BOTTOM_BACK, object_type)
        # self.load_model(get_undead_skeleton_halberd(), GameConstants.COMPUTER_TOP_FRONT, object_type, flip_x=True)
        # self.load_model(get_undead_skeleton_halberd(), GameConstants.COMPUTER_MIDDLE_FRONT, object_type, flip_x=True)
        # self.load_model(get_undead_skeleton_halberd(), GameConstants.COMPUTER_BOTTOM_FRONT, object_type, flip_x=True)
        # self.load_model(get_empire_swordsman(), GameConstants.COMPUTER_TOP_FRONT, object_type, flip_x=False)
        # self.load_model(get_empire_swordsman(), GameConstants.COMPUTER_MIDDLE_FRONT, object_type, flip_x=False)
        # self.load_model(get_empire_swordsman(), GameConstants.COMPUTER_BOTTOM_FRONT, object_type, flip_x=False)

        self.load_model(get_dwarf_hero(), GameConstants.COMPUTER_TOP_FRONT, object_type, flip_x=True)
        self.load_model(get_dwarf_hero(), GameConstants.COMPUTER_MIDDLE_FRONT, object_type, flip_x=True)
        self.load_model(get_dwarf_hero(), GameConstants.COMPUTER_BOTTOM_FRONT, object_type, flip_x=True)

        tm = self.__turn_manager

        for model in self.__turn_manager.get_all_models_list():
            if model.get_type() == GameConstants.PLAYER_GAME_OBJECTS:
                unit = tm.get_all_player_models()
                enemy_unit = tm.get_all_computer_models()
            else:
                unit = tm.get_all_computer_models()
                enemy_unit = tm.get_all_player_models()
            for sr in model.get_special_rules_list():
                sr.on_init(model, unit, enemy_unit)

        return

    def load_model(self, model, position, object_type, flip_x=False):
        size = model.get_size()

        new_position = (position[0] - size[0] / 2, position[1] - size[1] / 2)  # position is center, need compensate
        model.set_position(new_position)
        model.set_type(object_type)

        if flip_x:
            model.flip_x()

        # self.add_scene_object(character)  # add to scene objects list
        if object_type == GameConstants.PLAYER_GAME_OBJECTS:
            self.__turn_manager.add_player_model(model)
        elif object_type == GameConstants.COMPUTER_GAME_OBJECTS:
            self.__turn_manager.add_computer_model(model)
        self.get_game().add_sprite_to_group(model, object_type)  # add to game engine sprites group
        return

    def create_background(self):
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

        self.get_game().set_background(surface)
        return

    def play_computer_turn(self, model):
        model_actions_list = model.get_actions_list()
        for action in model_actions_list:
            if type(action) == Attack or type(action) == RangeAttack:
                break
        # self.__current_action.set_action(action)
        self.__action_manager.set_action(action)
        targets = self.__turn_manager.get_all_player_models()
        # TODO: improve the target selection process, lowest WS/ lowest wounds/...
        if not any(targets):
            return
        target = targets[0]
        # self.__current_action.set_targets(target)
        self.__action_manager.set_targets(target)
        return
