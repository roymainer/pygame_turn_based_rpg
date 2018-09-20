"""
Turn Manager

Handles the models turns in each phase
1. update current model
2.

"""
from Managers.Manager import Manager, TURN_MANAGER
from Shared.Action import Attack, RangeAttack  # , Spells, Skills, Items, Skip
from Shared.Model import Model
import logging
logger = logging.getLogger().getChild(__name__)


def reblit_special_rules(game_engine, model_manager):
    logger.info("Updating special rules on screen")
    for model in model_manager.get_all_models_sorted_list():
        model.clear_models_special_rules()  # hide previous special rules
        model.special_rules_to_texts()
        for text in model.get_special_rules_texts():
            game_engine.add_sprite_to_group(text, 0)


# noinspection PyMethodMayBeStatic
class TurnManager(Manager):

    def __init__(self, scene):
        logger.info("Init")
        self.__player_turn = True  # TODO: maybe roll a dice to see who starts first?
        self.__current_model_index = 0
        self.__current_model = None

        super(TurnManager, self).__init__(scene, TURN_MANAGER)

    def update(self):

        if self.__are_models_actions_ready():
            # if all models are ready (with assigned actions and targets)

            # acquire the lock from Events Manager, no need to register any more user events
            if not self.__acquire_lock_from_events_manager():
                # if unable to get the lock
                return

            # event_manager = self.get_events_manager()
            game_engine = self.get_game_engine()
            action_manager = self.get_action_manager()
            model_manager = self.get_models_manager()
            phase_manager = self.get_phase_manager()
            ui_manager = self.get_ui_manager()

            ui_manager.remove_player_markers()  # hide player markers once action starts
            ui_manager.remove_computer_markers()  # hide computer markers

            """ Update current model"""
            current_model = self.__update_current_model()

            self.__perform_models_action(action_manager, current_model, game_engine, model_manager)

            """ Animate targets death """
            if current_model.is_animation_cycle_done():
                logger.info("{} {} animation finished".format(current_model.get_name(), current_model.get_animation()))
                self.__current_model.set_action_animation_done()

                """ Clear last action text """
                logger.info("Clearing models action results texts")
                for model in model_manager.get_all_models_sorted_list():
                    model.clear_action_results_texts()

                self.animate_death_and_remove_killed_models(model_manager, phase_manager)

                """ wait for models to finish their animations """
                # first make sure all models finished their animation cycle
                non_played_models = model_manager.get_all_models_sorted_list()
                non_played_models.remove(current_model)
                for model in non_played_models:
                    if not model.is_animation_cycle_done():
                        return

                """ Check if phase is complete """
                if phase_manager.is_phase_complete():
                    self.release_lock(__name__)

                else:
                    """ Advance to next model """
                    logger.info("All models finished their animation cycle")
                    self.__set_next_model_index()


    def animate_death_and_remove_killed_models(self, model_manager, phase_manager):
        """ Animate death and remove killed models """
        all_models = model_manager.get_all_models_sorted_list()
        target = None
        for model in all_models:
            if model.is_killed():
                logger.info("{} is killed, setting animation to 'die'".format(model.get_name()))
                model.set_animation("die")  # animate death on all killed models
                target = model
            else:
                model.set_animation("idle")  # return all remaining models to idle state
        if target is not None:
            if target.is_animation_cycle_done():
                logger.info("{} {} animation finished".format(target.get_name(), target.get_animation()))

                # """ Clear last action text """
                # logger.info("Clearing models action results texts")
                # for model in model_manager.get_all_models_sorted_list():
                #     model.clear_action_results_texts()

                """ clear all dead models """
                model_manager.remove_dead_models()

                """ Refresh current phase models list """
                phase_manager.refresh_current_phase_models_list()

    def __perform_models_action(self, action_manager, current_model, game_engine, model_manager):
        """ Perform models action """
        if current_model.is_action_ready() and not current_model.is_action_done():
            # if current model is ready to perform action and unless action is done, perform action
            logger.info("{} is ready to act".format(current_model.get_name()))
            action_manager.perform_action(current_model)

            # """ Display special rules """
            # reblit_special_rules(game_engine, model_manager)

            """ Blit action results texts"""
            for model in model_manager.get_all_models_sorted_list():
                for text in model.get_action_results_texts():
                    game_engine.add_sprite_to_group(text)

    def __update_current_model(self):
        current_model = self.get_current_model()
        if current_model != self.__current_model:
            logger.info("Current models's turn:   {}".format(current_model.get_name()))
            self.__current_model = current_model  # update current model

            """ Set computer model action and targets"""
            if not current_model.is_player_model():
                self.play_computer_turn(current_model)
        return current_model

    def __are_models_actions_ready(self):
        phase_manager = self.get_phase_manager()
        # models_list = phase_manager.get_current_phase_models_list()
        models_list = phase_manager.get_current_phase_player_models_list()

        if not any(models_list):
            # return False
            return True  # can still play computer's turn

        for model in models_list:
            if not model.is_action_ready():
                return False
        return True

    def __are_models_actions_complete(self):
        phase_manager = self.get_phase_manager()
        models_list = phase_manager.get_current_phase_models_list()
        # models_list = phase_manager.get_current_phase_player_models_list()

        if not any(models_list):
            return True

        for model in models_list:
            if not model.is_action_complete():
                return False
        return True

    def __acquire_lock_from_events_manager(self) -> bool:
        if self.acquire_lock(__name__):
            # if lock belongs to Turn Manager,
            return True

        # if not, since the models are ready, release the lock from Events Manager
        if self.release_lock("Managers.EventsManager"):
            # and acquire it
            return self.acquire_lock(__name__)
        else:
            return False

    def set_current_model_index(self, index):
        self.__current_model_index = index

    def reset_current_model(self):
        self.__current_model_index = 0
        self.__current_model = None

    def get_current_model(self) -> Model:
        phase_manager = self.get_phase_manager()
        current_phase_models_list = phase_manager.get_current_phase_models_list()
        try:
            current_model = current_phase_models_list[self.__current_model_index]
        except:
            print("Error")
        return current_model

    def get_model_unit(self, model=None):
        mm = self.get_models_manager()
        if model is None:
            model = self.get_current_model()
        return mm.get_model_unit(model)

    def get_opponent_unit(self, model=None):
        mm = self.get_models_manager()
        if model is None:
            model = self.get_current_model()
        return mm.get_opponent_unit(model)

    def __set_next_model_index(self) -> None:
        logger.info("Set next model index")
        phase_manager = self.get_phase_manager()
        current_phase_models_list = phase_manager.get_current_phase_models_list()
        self.__current_model_index += 1
        if self.__current_model_index not in range(len(current_phase_models_list)):
            self.__current_model_index = 0

    def play_computer_turn(self, model):
        logger.info("Playing Computer Turn")
        # TODO: need to move to AI manager, send phase as parameter...

        phase_manager = self.get_phase_manager()

        action = Attack()  # default action

        # set model action
        model_actions_list = phase_manager.get_current_phase_actions_list()
        for action in model_actions_list:
            if type(action) == Attack or type(action) == RangeAttack:
                break
        model.set_action(action)

        # set action targets
        mm = self.get_models_manager()
        targets = mm.get_player_sorted_models_list()
        # TODO: improve the target selection process, lowest WS/ lowest wounds/...
        if not any(targets):
            return
        target = targets[0]
        model.set_targets(target)
        model.set_action_ready()
        return
