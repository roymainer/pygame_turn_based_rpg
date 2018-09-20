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
        self.__animation = None
        self.set_animation("idle")  # all animated objects start at idle
        image = self.__animator.get_sprite_by_key(self.__animation)
        super(AnimatedObject, self).__init__(image, position, object_type)

        self.__speed = (0, 0)

    def __repr__(self) -> str:
        return "AnimatedObject"

    # def update(self, seconds):
    def update(self):

        if self.get_animation() == "die" and self.is_animation_cycle_done():
            # if the model died and finished the animation cycle, don't update image to next sprite
            return

        self.image = self.__animator.get_sprite_by_key(self.__animation)

    # def set_speed(self, speed) -> int:
    #     self.__speed = speed
    #
    # def get_speed(self):
    #     return self.__speed

    def set_animation(self, animation) -> None:
        if animation not in self.get_animations_list():
            self.__animation = self.__animations_list[0]
        if animation != self.__animation:
            self.__animator.reset_animation()
            self.__animation = animation

    def get_animation(self) -> str:
        return self.__animation

    def is_animation_cycle_done(self) -> bool:
        return self.__animator.is_animation_cycle_done()

    def set_last_animation(self) -> None:
        self.__animator.set_last_animation()

    def get_animations_list(self) -> list:
        return self.__animator.get_animations_keys()

    def flip_x(self) -> None:
        self.__animator.set_flip()
