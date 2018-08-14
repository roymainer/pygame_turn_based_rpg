"""
Character class is an extension of the AnimatedObject class
it supports more actions (animations), character attributes and sounds (need to add)
"""


from Shared.AnimatedObject import AnimatedObject
from Shared.Bestiary import Bestiary


class Character(AnimatedObject):

    def __init__(self, attributes, spritesheet_file, size, position, object_type):
        super(Character, self).__init__(spritesheet_file, size, position, object_type)
        self.set_action("idle")  # every character must have idle stance!

        # TODO: instead of loading from a py file need to load from an encrypted file
        # TODO: save the entire dictionary as a private member instead of breaking it down
        self.__attributes = attributes
        self.__current_wounds = self.get_max_wounds()

    def __repr__(self):
        return "Character"

    def get_name(self):
        return self.__attributes[Bestiary.NAME]

    def get_move(self):
        return self.__attributes[Bestiary.M]

    def get_weapon_skill(self):
        return self.__attributes[Bestiary.WS]

    def get_ballistic_skill(self):
        return self.__attributes[Bestiary.BS]

    def get_strength(self):
        return self.__attributes[Bestiary.S]

    def get_toughness(self):
        return self.__attributes[Bestiary.T]

    def get_wounds(self):
        return self.__current_wounds

    def get_max_wounds(self):
        return self.__attributes[Bestiary.W]

    def get_initiative(self):
        return self.__attributes[Bestiary.I]

    def get_attacks(self):
        return self.__attributes[Bestiary.A]

    def get_leadership(self):
        return self.__attributes[Bestiary.LD]

    def get_unit_type(self):
        return self.__attributes[Bestiary.UNIT_TYPE]
