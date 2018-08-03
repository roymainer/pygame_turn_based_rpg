"""
Character class is an extension of the AnimatedObject class
it supports more actions (animations), character attributes and sounds (need to add)
"""


from Shared.AnimatedObject import AnimatedObject


class Character(AnimatedObject):

    def __init__(self, spritesheet_file, size, position, object_type):
        super(Character, self).__init__(spritesheet_file, size, position, object_type)
        self.set_action("idle") # every character must have idle stance!

    def __repr__(self):
        return "Character"
