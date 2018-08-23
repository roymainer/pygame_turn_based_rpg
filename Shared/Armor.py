# TODO: need to be a GameObject
from Shared.Attibutes import Attributes


class Armor:

    def __init__(self, name="", ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0, req_roll=7, to_hit_re_roll=0):
        self.__attributes = Attributes(name, ws, bs, s, t, w, i, a, ld)
        self.__armor_save_req_roll = req_roll
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

    def get_required_roll(self):
        return self.__armor_save_req_roll

    def get_to_hit_re_roll(self):
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll


# ARMOR_NONE = Armor(name="None", ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0, req_roll=7, to_hit_re_roll=0)
ARMOR_NONE = Armor(name="None", req_roll=7)
LIGHT_ARMOR = Armor(name="Light Armor", req_roll=6)
HEAVY_ARMOR = Armor(name="Heavy Armor", req_roll=5)
CHAOS_ARMOR = Armor(name="Chaos Armor", req_roll=5)
DRAGON_ARMOR = Armor(name="Dragon Armor", req_roll=5)
