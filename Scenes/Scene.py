

class Scene:

    def __init__(self, game_engine):
        self.__game_engine = game_engine  # save the game class/engine
        # self.__scene_objects = []

    def get_game_engine(self):
        return self.__game_engine

    def handle_events(self):
        """ Abstract method to handle events """
        pass
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.__game_engine.stop()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             self.__game_engine.stop()

    def update(self):
        """ Abstract method to update scene elements """
        pass

    # def on_exit(self):
    #     """ Abstract method called on scene exit """
    #     pass

    # def add_text(self, string, position, color=(255, 255, 255), background=(0, 0, 0),
    #              size=UIConstants.FONT_SIZE_SMALL):
    #     self.__texts.append(Text(string, position, color, background, size))
    #
    # def add_scene_object(self, game_object):
    #     self.__scene_objects.append(game_object)
    #
    # def get_scene_objects_list(self):
    #     return self.__scene_objects
