from Shared.Character import Character
from Shared.GameConstants import GameConstants


def load_character(game_engine, scene, key, position):
    key = key.lower()
    sprite_sheet = Util.GAME_OBJECTS_DICT[key]["sprite_sheet"]
    size = Util.GAME_OBJECTS_DICT[key]["size"]
    new_position = (position[0] - size[0] / 2, position[1] - size[1] / 2)

    character = Character(sprite_sheet, size, new_position)  # init adventurer

    scene.add_game_object(character)  # add to scene objects list
    game_engine.add_sprite_to_group(character)  # add to game engine sprites group
    return


class Util:

    GAME_OBJECTS_DICT = {
        "adventurer":
            {"sprite_sheet": GameConstants.ADVENTURER_SPRITE_SHEET,
             "size": GameConstants.ADVENTURER_SIZE},
        "slime":
            {"sprite_sheet": GameConstants.SLIME_SPRITE_SHEET,
             "size": GameConstants.SLIME_SIZE}
    }
