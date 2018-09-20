from Managers.Manager import Manager, MAGIC_MANAGER
from Shared.Rolls import get_d6_roll
import logging
logger = logging.getLogger().getChild(__name__)


class MagicManager(Manager):

    def __init__(self, scene):
        logger.info("Init")
        self.__player_power_pool = 0
        self.__player_dispel_pool = 0
        self.__computer_power_pool = 0
        self.__computer_dispel_pool = 0

        super(MagicManager, self).__init__(scene, MAGIC_MANAGER)

    # ----- MAGIC PHASE (WHFB Rule Book 8th ed. p.30) ----- #
    def roll_for_winds_of_magic(self):
        logger.info("Roll for winds of magic")
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

        logger.info("Player Power Pool: {}".format(self.__player_power_pool))
        logger.info("Player Dispel Pool: {}".format(self.__player_dispel_pool))
        logger.info("Computer Power Pool: {}".format(self.__computer_power_pool))
        logger.info("Computer Dispel Pool: {}".format(self.__computer_dispel_pool))

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

    def get_player_power_pool(self):
        return self.__player_power_pool

    def set_player_power_pool(self, pp):
        logger.info("Set player power pool: {}".format(pp))

        self.__player_power_pool = pp

    def get_player_dispel_pool(self):
        return self.__player_dispel_pool

    def set_player_dispel_pool(self, dp):
        logger.info("Set player dispel pool: {}".format(dp))
        self.__player_dispel_pool = dp

    def get_computer_power_pool(self):
        return self.__computer_power_pool

    def set_computer_power_pool(self, pp):
        logger.info("Set computer power pool: {}".format(pp))
        self.__computer_power_pool = pp

    def get_computer_dispel_pool(self):
        return self.__computer_dispel_pool

    def set_computer_dispel_pool(self, dp):
        logger.info("Set computer dispel pool: {}".format(dp))
        self.__computer_dispel_pool = dp
