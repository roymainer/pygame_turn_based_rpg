from UI.PlayingGameSceneUI import COMPUTER_MODELS_MENU, SKILLS_MENU, SPELLS_MENU, ITEMS_MENU


class Action:

    def __init__(self, name=""):
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def get_menu_item_string(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return self.__name

    def get_next_menu(self) -> int:
        pass

    # def on_click(self, model, targets):
    #     pass


class Attack(Action):

    ATTACK_TYPE_NORMAL = 0
    ATTACK_TYPE_STOMP = 1
    ATTACK_TYPE_THUNDERSTOMP = 2
    ATTACK_TYPE_BREATH = 3

    def __init__(self):
        super(Attack, self).__init__("Attack")
        self.__attack_type = Attack.ATTACK_TYPE_NORMAL

    def get_attack_type(self):
        return self.__attack_type

    def set_attack_type(self, attack_type):
        self.__attack_type = attack_type

    def get_next_menu(self) -> int:
        return COMPUTER_MODELS_MENU
    
    
class RangeAttack(Action):
    
    def __init__(self):
        super(RangeAttack, self).__init__("Shoot")

    def get_next_menu(self) -> int:
        return COMPUTER_MODELS_MENU


class Skills(Action):
    
    def __init__(self):
        super(Skills, self).__init__("Skills")

    def get_next_menu(self) -> int:
        return SKILLS_MENU


class Spells(Action):

    def __init__(self):
        super(Spells, self).__init__("Spells")

    def get_next_menu(self) -> int:
        return SPELLS_MENU


class Items(Action):

    def __init__(self):
        super(Items, self).__init__("Items")

    def get_next_menu(self) -> int:
        return ITEMS_MENU
