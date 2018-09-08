from Shared.Attributes import Attributes


class Armor(Attributes):

    def __init__(self, name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0, req_roll=7, to_hit_re_roll=False):
        super(Armor, self).__init__(name, m, ws, bs, s, t, w, i, a, ld)

        self.__armor_save_req_roll = req_roll
        self.__to_hit_re_roll = to_hit_re_roll

    def get_required_roll(self) -> int:
        return self.__armor_save_req_roll

    def get_to_hit_re_roll(self) -> bool:
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll


class LightArmor(Armor):
    def __init__(self):
        super(LightArmor, self).__init__(name="Light Armor", req_roll=6)


class HeavyArmor(Armor):
    def __init__(self):
        super(HeavyArmor, self).__init__(name="Heavy Armor", req_roll=5)


class ChaosArmor(Armor):
    def __init__(self):
        super(ChaosArmor, self).__init__(name="Chaos Armor", req_roll=5)


class DragonArmor(Armor):
    def __init__(self):
        super(DragonArmor, self).__init__(name="Dragon Armor", req_roll=5)
