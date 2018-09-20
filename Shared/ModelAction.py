class ModelAction:

    def __init__(self):
        self.__action = None
        self.__targets = None
        self.__action_ready = False
        self.__action_done = False
        self.__animation_done = False
        self.__miscast = False

    # -------- ACTION -------- #
    def set_action(self, action):
        self.__action = action

    def get_action(self):
        return self.__action

    def set_targets(self, targets):
        self.__targets = targets

    def get_targets(self):
        return self.__targets

    def set_action_ready(self):
        self.__action_ready = True

    def unset_action_ready(self):
        self.__action_ready = False

    def is_action_ready(self):
        return self.__action_ready

    def set_action_done(self):
        self.__action_done = True

    def unset_action_done(self):
        self.__action_done = False

    def is_action_done(self):
        return self.__action_done

    def set_action_animation_done(self):
        self.__animation_done = True

    def unset_action_animation_done(self):
        self.__animation_done = False

    def is_action_animation_done(self):
        return self.__animation_done

    def set_miscast(self):
        self.__miscast = True

    def unset_miscast(self):
        self.__miscast = False

    def did_spell_miscast(self):
        return self.__miscast

    def is_action_complete(self):
        return self.is_action_ready() and self.is_action_done() and self.is_action_animation_done()

    def reset_action(self):
        self.__action = None
        self.__targets = None
        self.unset_action_ready()
        self.unset_action_done()
        self.unset_action_animation_done()
        self.unset_miscast()
