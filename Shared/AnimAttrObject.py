from Shared.AnimatedObject import AnimatedObject


class AnimAttrObject(AnimatedObject):
    
    def __init__(self, sprite_sheet_file, size, position, object_type,
                 name="", m=0, ws=0, bs=0, s=0, t=0, w=0, i=0, a=0, ld=0):
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

    def get_name(self):
        return self.__name

    def get_move(self):
        return self.__M

    def get_weapon_skill(self):
        return self.__WS

    def get_ballistic_skill(self):
        return self.__BS

    def get_strength(self):
        return self.__S

    def get_toughness(self):
        return self.__T

    def get_wounds(self):
        return self.__W

    def get_initiative(self):
        return self.__I

    def get_attack(self):
        return self.__A

    def get_leadership(self):
        return self.__LD
