from GameEngine import GameEngine


class RPG:

    def __init__(self):
        self.__game_engine = GameEngine()
        self.__game_engine.start()


RPG()
