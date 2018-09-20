from Phases.Phase import Phase, MAGIC_PHASE, SHOOTING_PHASE
from Shared.Action import Spells, Skip
import logging
logger = logging.getLogger().getChild(__name__)


def model_finished_casting(model, power_pool) -> bool:
    if model.did_spell_miscast():
        # if last spell was miscast
        return True

    if isinstance(model.get_action(), Skip):
        # if model action is Skip
        return True

    remaining_spells = model.get_uncast_spells_list()
    if not any(remaining_spells):
        # if all of the wizards spells were cast
        return True

    # if the minimum required dice for any of the uncast spells is less than the power pool
    min_req_dice = 12
    for rs in remaining_spells:
        min_req_dice = min(min_req_dice, rs.get_cost())

    if power_pool * 6 < min_req_dice:
        return True

    return False


class MagicPhase(Phase):

    def __init__(self, phase_manager):
        logger.info("Init")
        super(MagicPhase, self).__init__(phase_manager, MAGIC_PHASE)
        self.refresh_models_list()  # get wizards from models list
        self.__next_phase_key = SHOOTING_PHASE

    def refresh_models_list(self):
        self.get_wizards_list()

    def is_phase_complete(self):
        if not super(MagicPhase, self).is_phase_complete():
            return False

        # if all models finished their actions and animations, check if they finished casting
        for wizard in self.get_models_list():
            if wizard.is_player_model():
                power_pool = self.get_player_power_pool()
            else:
                power_pool = self.get_computer_power_pool()

            if not model_finished_casting(wizard, power_pool):
                # if any of the wizard has more spells to cast, repeat the magic phase
                self.__next_phase_key = MAGIC_PHASE
                break

        # phase complete
        return True

    def get_phase_actions_list(self, turn_manager) -> list:
        actions_list = super(MagicPhase, self).get_phase_actions_list(turn_manager)
        actions_list.insert(0, Spells())
        return actions_list

    def get_next_phase_key(self):
        return self.__next_phase_key
