class UnitAction:

    def __init__(self, unit, action=None, targets=[]):
        self.__unit = unit
        self.__action = action
        self.__targets = targets

    def get_unit(self):
        return self.__unit

    def set_action(self, action):
        self.__action = action

    def get_action(self):
        return self.__action

    def set_targets(self, targets):
        if type(targets) is list:
            self.__targets = targets
        else:
            self.__targets = [targets]

    def get_targets(self):
        return self.__targets

    def is_ready(self):
        if self.__unit is not None and self.__action is not None and any(self.__targets):
            return True
        else:
            return False

    def perform_action(self):
        # TODO: finish this
        print("Perform Action")
        pass
