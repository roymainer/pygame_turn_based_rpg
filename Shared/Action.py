class Action:

    def __init__(self, name=""):
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def get_menu_item_string(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return self.__name


class Attack(Action):

    ATTACK_TYPE_NORMAL = 0
    ATTACK_TYPE_STOMP = 1
    ATTACK_TYPE_THUNDER_STOMP = 2
    ATTACK_TYPE_BREATH = 3

    def __init__(self):
        super(Attack, self).__init__("Attack")
        self.__attack_type = Attack.ATTACK_TYPE_NORMAL

    def get_attack_type(self):
        return self.__attack_type

    def set_attack_type(self, attack_type):
        self.__attack_type = attack_type


class RangeAttack(Action):
    
    def __init__(self):
        super(RangeAttack, self).__init__("Shoot")


class Skills(Action):
    
    def __init__(self):
        super(Skills, self).__init__("Skills")


class Spells(Action):

    def __init__(self):
        super(Spells, self).__init__("Spells")


class Items(Action):

    def __init__(self):
        super(Items, self).__init__("Items")


class Skip(Action):
    """
    Skip action is used to pass the turn to the next model.
    For example on Magic Phase if the player doesn't want to cast a spell
    """
    def __init__(self):
        super(Skip, self).__init__("Skip")

