"""
AnimatedObject is a child class of GameObject
The different is it has an Animator object and it loads a sprite sheet instead of a single image
"""

from Shared.GameObject import GameObject
from Shared.Animator import Animator


class AnimatedObject(GameObject):

    def __init__(self, sprite_sheet_file, size, position, object_type):

        self.__animator = Animator(sprite_sheet_file, sprite_size=size)
        self.__animations_list = self.__animator.get_animations_keys()
        # self.__action = self.__actions_list[0]  # default single animation for objects
        self.__action = None
        self.set_action("idle")  # all animated objects start at idle
        image = self.__animator.get_next_sprite(self.__action)
        super(AnimatedObject, self).__init__(image, position, object_type)

        self.__speed = (0, 0)

    def __repr__(self):
        return "AnimatedObject"

    # def update(self, seconds):
    def update(self):

        if self.get_action() == "die" and self.is_animation_cycle_done():
            # if the model died and finished the animation cycle, don't update image to next sprite
            return

        self.image = self.__animator.get_next_sprite(self.__action)

    def set_speed(self, speed):
        self.__speed = speed

    def get_speed(self):
        return self.__speed

    def set_action(self, action):
        if action not in self.get_animations_list():
            self.__action = self.__animations_list[0]
        if action != self.__action:
            self.__animator.reset_animation()
            self.__action = action

    def get_action(self):
        return self.__action

    def is_animation_cycle_done(self):
        return self.__animator.is_animation_cycle_done()

    def set_last_animation(self):
        self.__animator.set_last_animation()

    def get_animations_list(self):
        return self.__animator.get_animations_keys()

    def flip_x(self):
        self.__animator.set_flip()
