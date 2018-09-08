from Shared.AnimatedObject import AnimatedObject

# Troop Types key
TT_IN = "Infantry"
TT_WB = "War Beast"
TT_CA = "Cavalry"
TT_MI = "Monstrous Infantry"
TT_MB = "Monstrous Beast"
TT_MC = "Monstrous Cavalry"
TT_MO = "Monster"
TT_CH = "Chariot"
TT_SW = "Swarms"
TT_UN = "Unique"
TT_WM = "War Machine"


class AnimAttrObject(AnimatedObject):
    
    def __init__(self, sprite_sheet_file=None, size=None, position=None, object_type=None,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0, tt=TT_IN):
        super(AnimAttrObject, self).__init__(sprite_sheet_file, size, position, object_type)

        self.__name = name
        self.__M = m
        self.__WS = ws
        self.__BS = bs
        self.__S = s
        self.__T = t
        self.__W = w
        self.__I = i
        self.__A = a
        self.__LD = ld
        self.__TT = tt

        self.__special_rules_list = []  # both models and weapons/armor have special rules

    def get_name(self) -> str:
        return self.__name

    def get_menu_item_string(self) -> str:
        # returns a string to be shown as a menu item
        return self.__name

    def get_move(self) -> int:
        return self.__M

    def get_weapon_skill(self) -> int:
        return self.__WS

    def get_ballistic_skill(self) -> int:
        return self.__BS

    def get_strength(self) -> int:
        return self.__S

    def get_toughness(self) -> int:
        return self.__T

    def get_wounds(self) -> int:
        return self.__W

    def get_initiative(self) -> int:
        return self.__I

    def get_attacks(self) -> int:
        return self.__A

    def get_leadership(self) -> int:
        return self.__LD

    def get_troop_type(self) -> str:
        return self.__TT

    def get_special_rules_list(self) -> list:
        return self.__special_rules_list

    def add_special_rule(self, special_rule) -> None:
        self.__special_rules_list.append(special_rule)

    def clear_used_up_special_rules(self) -> None:
        # remove all special rules that are one times and were used in the previous action phase
        srl = [x for x in self.__special_rules_list if not x.is_used_up()]
        self.__special_rules_list = srl
