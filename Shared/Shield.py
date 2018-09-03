from Shared.Attributes import Attributes


class Shield(Attributes):

    def __init__(self, name="Shield", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 save_modifier=-1, to_hit_re_roll=0):
        super(Shield, self).__init__(name, m, ws, bs, s, t, w, i, a, ld)

        self.__save_modifier = save_modifier
        self.__to_hit_re_roll = to_hit_re_roll

    def get_shield_save_modifier(self) -> int:
        return self.__save_modifier

    def get_to_hit_re_roll(self) -> int:
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll
