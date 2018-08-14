"""
AnimatedObject is a child class of GameObject
The different is it has an Animator object and it loads a sprite sheet instead of a single image
"""

from Shared.GameObject import GameObject
from Shared.Animator import Animator


class AnimatedObject(GameObject):

    def __init__(self, sprite_sheet_file, size, position, object_type):

        self.__animator = Animator(sprite_sheet_file, sprite_size=size)
        self.__actions_list = self.__animator.get_animations_keys()
        self.__action = self.__actions_list[0]  # default single animation for objects
        image = self.__animator.get_next_sprite(self.__action)
        super(AnimatedObject, self).__init__(image, position, object_type)

        self.__speed = (0, 0)

    def __repr__(self):
        return "AnimatedObject"

    # def update(self, seconds):
    def update(self):
        self.image = self.__animator.get_next_sprite(self.__action)

        if self.__speed[0] < 0:  # move left
            self.__animator.set_flip()
        elif self.__speed[0] > 0:
            self.__animator.unset_flip()

        x = self.rect.x
        y = self.rect.y

        self.set_position((x + self.__speed[0], y + self.__speed[1]))  # update position

    def set_speed(self, speed):
        self.__speed = speed

    def get_speed(self):
        return self.__speed

    def set_action(self, action):
        if action not in self.get_actions_list():
            return
        self.__action = action

    def get_action(self):
        return self.__action

    def get_actions_list(self):
        return self.__animator.get_animations_keys()

    def turn_right(self):
        self.__animator.unset_flip()

    def turn_left(self):
        self.__animator.set_flip()
