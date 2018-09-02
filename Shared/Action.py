from UI.PlayingGameSceneUI import COMPUTER_MODELS_MENU, SKILLS_MENU, SPELLS_MENU, ITEMS_MENU


class Action:

    def __init__(self, name=""):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_menu_item_string(self):
        return self.__name

    def __repr__(self):
        return self.__name

    def get_next_menu(self):
        pass

    def on_click(self, model, targets):
        pass


class Attack(Action):

    def __init__(self):
        super(Attack, self).__init__("Attack")

    def get_next_menu(self):
        return COMPUTER_MODELS_MENU
    
    
class RangeAttack(Action):
    
    def __init__(self):
        super(RangeAttack, self).__init__("Shoot")

    def get_next_menu(self):
        return COMPUTER_MODELS_MENU


class Skills(Action):
    
    def __init__(self):
        super(Skills, self).__init__("Skills")

    def get_next_menu(self):
        return SKILLS_MENU


class Spells(Action):

    def __init__(self):
        super(Spells, self).__init__("Spells")

    def get_next_menu(self):
        return SPELLS_MENU


class Items(Action):

    def __init__(self):
        super(Items, self).__init__("Items")

    def get_next_menu(self):
        return ITEMS_MENU
