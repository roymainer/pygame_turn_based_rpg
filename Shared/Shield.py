from Shared.Attibutes import Attributes


class Shield:
    
    def __init__(self, name="", ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0, save_modifier=0, to_hit_re_roll=0):
        self.__attributes = Attributes(name, ws, bs, s, t, w, i, a, ld)
        self.__save_modifier = save_modifier
        self.__to_hit_re_roll = to_hit_re_roll

    def get_name(self):
        return self.__attributes.get_name()

    def get_weapon_skill(self):
        return self.__attributes.get_weapon_skill()

    def get_ballistic_skill(self):
        return self.__attributes.get_ballistic_skill()

    def get_strength(self):
        return self.__attributes.get_strength()

    def get_wounds(self):
        return self.__attributes.get_wounds()

    def get_initiative(self):
        return self.__attributes.get_initiative()

    def get_attack(self):
        return self.__attributes.get_attack()

    def get_leadership(self):
        return self.__attributes.get_leadership()

    def get_armor_save_modifier(self):
        return self.__save_modifier

    def get_to_hit_re_roll(self):
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll


SHIELD_NONE = Shield(name="None")
SHIELD = Shield(name="Shield", save_modifier=-1)
