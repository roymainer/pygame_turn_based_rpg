"""
Phase Manager

Handles the turn different phases:
1. Movement (irrelevant for this game)
2. Magic
3. Shooting
4. Close Combat

Each phase has it own active models and it's own actions

Once all models finished their actions, the phase ends and the next phase starts
"""
from Managers.Manager import Manager, PHASE_MANAGER
from Shared.Action import Attack, RangeAttack, Spells, Skills, Items, Skip
from Shared.GameConstants import WHITE, SCREEN_SIZE
from Shared.Rolls import get_2d6_roll, get_d6_roll
from UI.Text import Text

MAGIC_PHASE = "Magic Phase"
SHOOTING_PHASE = "Shooting Phase"
CLOSE_COMBAT_PHASE = "Close Combat Phase"

PHASES = [MAGIC_PHASE, SHOOTING_PHASE, CLOSE_COMBAT_PHASE]


class PhaseManager(Manager):

    def __init__(self, scene):

        self.__current_phase_index = -1
        self.__current_phase_models_list = []  # repopulate with appropriate models whenever a phase changes
        self.__texts = []

        # Magic
        self.__player_power_pool = 0
        self.__player_dispel_pool = 0
        self.__computer_power_pool = 0
        self.__computer_dispel_pool = 0

        super(PhaseManager, self).__init__(scene, PHASE_MANAGER)

    def update(self):
        if self.is_phase_complete():
            self.set_next_phase()

    def __get_current_phase(self):
        return PHASES[self.__current_phase_index]

    def __set_phase(self) -> None:
        """
        Each new phase:
        reset all models actions
        get all models that are active in this phase
        * on new magic phase clear used up special rules
        reset current model index and set model to None
        :return:
        """
        tm = self.get_turn_manager()
        mm = self.get_models_manager()
        ui_manager = self.get_ui_manager()

        mm.reset_models_actions()  # reset all models actions at the start of the new phase

        self.get_current_phase_model_list(mm)
        if self.__get_current_phase() == MAGIC_PHASE:
            self.__roll_for_winds_of_magic()

        tm.set_current_model_index(0)
        tm.reset_current_model()
        ui_manager.update_all_menus()  # update models menus with current phase active units

    def get_current_phase_model_list(self, mm):
        # ----- MAGIC PHASE ----- #
        if self.__get_current_phase() == MAGIC_PHASE:
            self.__current_phase_models_list = mm.get_wizards_list()
            # clear all used up special rules at the start of the next magic phase
            mm.clear_used_up_special_rules()
        # ----- SHOOTING PHASE ----- #
        elif self.__get_current_phase() == SHOOTING_PHASE:
            self.__current_phase_models_list = mm.get_shooters_list()
        # ----- CLOSE COMBAT PHASE ----- #
        else:
            self.__current_phase_models_list = mm.get_all_models_sorted_list()

    def set_next_phase(self):
        self.__current_phase_index += 1
        if self.__current_phase_index >= len(PHASES):
            self.__current_phase_index = 0

        self.__set_phase()
        self.__add_phase_text()

    def is_phase_complete(self):
        models_manager = self.get_models_manager()
        self.get_current_phase_model_list(models_manager)  # need to update in case any unit died
        for model in self.__current_phase_models_list:
            if not model.is_action_done() or not model.is_animation_cycle_done():
                # if any of the models, didn't finish it's action and animation, the phase isn't done
                return False

        models_manager = self.get_models_manager()
        models_manager.remove_dead_models()

        return True

    def get_current_phase_models_list(self) -> list:
        return self.__current_phase_models_list

    def get_current_phase_player_models_list(self) -> list:
        all_models = self.get_current_phase_models_list()
        player_models = [x for x in all_models if x.is_player_model()]
        return player_models

    def get_current_phase_computer_models_list(self) -> list:
        all_models = self.get_current_phase_models_list()
        computer_models = [x for x in all_models if not x.is_player_model()]
        return computer_models

    def get_current_phase_actions_list(self) -> list:
        actions_list = [Items(), Skip()]
        if self.__get_current_phase() == MAGIC_PHASE:
            action = Spells()
        elif self.__get_current_phase() == SHOOTING_PHASE:
            action = RangeAttack()
        else:
            action = Attack()

        tm = self.get_turn_manager()
        current_model = tm.get_current_model()
        if any(current_model.get_skills_list()):
            actions_list.insert(0, Skills())

        actions_list.insert(0, action)
        return actions_list

    def __add_text(self, string):
        text = Text(string, (0, 0), WHITE, None, 28)
        text_size = text.get_size()
        position = (SCREEN_SIZE[0] / 2 - text_size[0]/2, 5)
        text.set_position(position)
        self.__texts.append(text)
        # game_engine = self.__scene.get_game_engine()
        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(text, 0)

    def __add_phase_text(self):
        self.__clear_texts()  # clear previous phase Text
        phase_string = self.__get_current_phase()
        self.__add_text(phase_string)

    def __clear_texts(self):
        for text in self.__texts:
            text.kill()
        self.__texts = []

    # ----- MAGIC PHASE (WHFB Rule Book 8th ed. p.30) ----- #
    def __roll_for_winds_of_magic(self):
        # player
        roll1 = get_d6_roll()
        roll2 = get_d6_roll()
        self.__player_power_pool = roll1 + roll2
        self.__player_dispel_pool = max(roll1, roll2)

        # computer
        roll1 = get_d6_roll()
        roll2 = get_d6_roll()
        self.__computer_power_pool = roll1 + roll2
        self.__computer_dispel_pool = max(roll1, roll2)

        self.__channeling_power_dice()
        self.__channeling_dispel_dice()

    def __channeling_power_dice(self):
        mm = self.get_models_manager()
        for wizard in mm.get_wizards_list():
            if get_d6_roll() == 6:
                if wizard.is_player_model():
                    self.__player_power_pool += 1
                else:
                    self.__computer_power_pool += 1

        # Power Limit WHFB p.30, number of dice can never exceed 12
        if self.__player_power_pool >= 12:
            self.__player_power_pool = 12
        if self.__computer_power_pool >= 12:
            self.__computer_power_pool = 12

    def __channeling_dispel_dice(self):
        mm = self.get_models_manager()
        for wizard in mm.get_wizards_list():
            if get_d6_roll() == 6:
                if wizard.is_player_model():
                    self.__player_dispel_pool += 1
                else:
                    self.__computer_dispel_pool += 1

        # Power Limit WHFB p.30, number of dice can never exceed 12
        if self.__player_dispel_pool >= 12:
            self.__player_dispel_pool = 12
        if self.__computer_dispel_pool >= 12:
            self.__computer_dispel_pool = 12
