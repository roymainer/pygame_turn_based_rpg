from Phases.Phase import Phase, SHOOTING_PHASE, CLOSE_COMBAT_PHASE
from Shared.Action import RangeAttack
import logging
logger = logging.getLogger().getChild(__name__)


class ShootingPhase(Phase):

    def __init__(self, phase_manager):
        logger.info("Init")
        super(ShootingPhase, self).__init__(phase_manager, SHOOTING_PHASE)
        self.refresh_models_list()  # get shooters from models manager

    def refresh_models_list(self):
        self.get_shooters_list()

    def get_phase_actions_list(self, turn_manager):
        actions_list = super(ShootingPhase, self).get_phase_actions_list(turn_manager)
        actions_list.insert(0, RangeAttack())
        return actions_list

    def get_next_phase_key(self):
        return CLOSE_COMBAT_PHASE
