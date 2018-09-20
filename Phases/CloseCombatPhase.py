from Phases.Phase import Phase, CLOSE_COMBAT_PHASE, MAGIC_PHASE
from Shared.Action import Attack
import logging
logger = logging.getLogger().getChild(__name__)


class CloseCombatPhase(Phase):

    def __init__(self, phase_manager):
        logger.info("Init")
        super(CloseCombatPhase, self).__init__(phase_manager, CLOSE_COMBAT_PHASE)
        self.refresh_models_list()  # get all models from models manager

    def refresh_models_list(self):
        self.get_all_models_list()

    def get_phase_actions_list(self, turn_manager):
        actions_list = super(CloseCombatPhase, self).get_phase_actions_list(turn_manager)
        actions_list.insert(0, Attack())
        return actions_list

    def get_next_phase_key(self):
        return MAGIC_PHASE
