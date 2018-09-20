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
from Phases.MagicPhase import MagicPhase
from Phases.Phase import MAGIC_PHASE, SHOOTING_PHASE
from Phases.ShootingPhase import ShootingPhase
from Phases.CloseCombatPhase import CloseCombatPhase
from Shared.GameConstants import GameConstants
from UI.Text import Text
import logging
logger = logging.getLogger().getChild(__name__)


class PhaseManager(Manager):

    def __init__(self, scene):
        logger.info("Init")
        self.__current_phase = None
        self.__texts = []

        super(PhaseManager, self).__init__(scene, PHASE_MANAGER)

    def on_init(self):
        # wizards = self.get_models_manager().get_wizards_list()
        # self.__current_phase = MagicPhase(self, wizards)
        self.__current_phase = MagicPhase(self)
        self.get_magic_manager().roll_for_winds_of_magic()  # roll for winds of magic
        self.get_ui_manager().update_all_menus()
        self.__add_phase_text()

    def update(self):
        if self.acquire_lock(__name__):
            phase_ready = self.set_next_phase()  # True if the phase is ready, meaning there are fitting models
            while not phase_ready:
                # if no models available proceed to next phase
                phase_ready = self.set_next_phase()

            ui_manager = self.get_ui_manager()
            turn_manager = self.get_turn_manager()

            # once a phase is set:
            turn_manager.set_current_model_index(0)  # set current model index to 0
            ui_manager.update_all_menus()  # update all menus

            self.release_lock(__name__)

    def __get_current_phase(self):
        return self.__current_phase

    def set_next_phase(self):

        models_manager = self.get_models_manager()

        next_phase_key = self.__current_phase.get_next_phase_key()

        if next_phase_key == MAGIC_PHASE:
            next_phase = MagicPhase

        elif next_phase_key == SHOOTING_PHASE:
            next_phase = ShootingPhase

        else:
            next_phase = CloseCombatPhase

        if isinstance(self.__current_phase, CloseCombatPhase) and next_phase_key == MAGIC_PHASE:
            models_manager.reset_spells()  # reset the wizards spell on NEW Magic Phase
            models_manager.clear_used_up_special_rules()  # clear special rules at start of next magic phase
            self.get_magic_manager().roll_for_winds_of_magic()  # roll for winds of magic

        # next_phase_obj = next_phase(self, models)  # init next phase
        next_phase_obj = next_phase(self)  # init next phase
        self.__current_phase = next_phase_obj
        if not any(next_phase_obj.get_models_list()):
            # if no models fit this phase, return False to skip to next phase
            return False

        models_manager.reset_models_actions()
        self.__add_phase_text()
        return True

    def is_phase_complete(self):
        return self.__current_phase.is_phase_complete()

    def refresh_current_phase_models_list(self) -> None:
        logger.info("Refresh current phase models list")
        self.__current_phase.refresh_models_list()

    def get_current_phase_models_list(self) -> list:
        return self.__current_phase.get_models_list()

    def get_current_phase_player_models_list(self) -> list:
        all_models = self.get_current_phase_models_list()
        player_models = [x for x in all_models if x.is_player_model() and not x.did_spell_miscast()]
        return player_models

    def get_current_phase_computer_models_list(self) -> list:
        all_models = self.get_current_phase_models_list()
        computer_models = [x for x in all_models if not x.is_player_model()]
        return computer_models

    def get_current_phase_actions_list(self) -> list:
        return self.__current_phase.get_phase_actions_list(self.get_turn_manager())

    def __add_text(self, string):
        text = Text(string, (0, 0), GameConstants.WHITE, None, 28)
        text_size = text.get_size()
        position = (GameConstants.SCREEN_SIZE[0] / 2 - text_size[0]/2, 5)
        text.set_position(position)
        self.__texts.append(text)
        game_engine = self.get_game_engine()
        game_engine.add_sprite_to_group(text, 0)

    def __add_phase_text(self):
        self.__clear_texts()  # clear previous phase Text
        phase_string = self.__current_phase.get_name()
        self.__add_text(phase_string)

    def __clear_texts(self):
        for text in self.__texts:
            text.kill()
        self.__texts = []
