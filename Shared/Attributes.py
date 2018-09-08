class Attributes:

    def __init__(self, name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0):
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

        self.__special_rules_list = []  # both models and weapons/armor have special rules

    def __repr__(self) -> str:
        return self.__name

    def get_name(self) -> str:
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

    def get_special_rules_list(self) -> list:
        return self.__special_rules_list

    def add_special_rule(self, special_rule) -> None:
        if special_rule in self.__special_rules_list:
            return
        self.__special_rules_list.append(special_rule)
