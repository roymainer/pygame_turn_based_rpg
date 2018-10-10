from GameEngine import GameEngine


class RPG:

    def __init__(self):
        self.__game_engine = GameEngine()

    def start(self):
        self.__game_engine.start()


def main():
    RPG().start()


main()
# import cProfile
# import re
#
# cProfile.run(main())
