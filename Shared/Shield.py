from Shared.AnimAttrObject import AnimAttrObject
from Shared.GameConstants import GameConstants


class Shield(AnimAttrObject):

    def __init__(self, sprite_sheet_file, size=None, position=(0, 0), object_type=GameConstants.ALL_GAME_OBJECTS,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0,
                 save_modifier=0, to_hit_re_roll=0):
        super(Shield, self).__init__(sprite_sheet_file, size, position, object_type, name, m, ws, bs, s, t, w, i, a, ld)

        self.__save_modifier = save_modifier
        self.__to_hit_re_roll = to_hit_re_roll

    def get_shield_save_modifier(self):
        return self.__save_modifier

    def get_to_hit_re_roll(self):
        # if the weapon grants a re-roll bonus to hit
        return self.__to_hit_re_roll
