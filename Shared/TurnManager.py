from Shared.Bestiary import UNIT_TYPE_MELEE, UNIT_TYPE_RANGE


class TurnManager:

    def __init__(self):
        self.__player_units = []  # used to keep player units in formation
        self.__computer_units = []  # used to keep computer units in formation
        self.__all_units_sorted = []  # all units sorted by initiative
        self.__current_unit = 0  # index to current turn's unit

    def __sort_all_units_list(self, sort_parameter: str= 'get_initiative'):
        # copy and exted both units lists into one
        all_units = list(self.__player_units)  # copy
        all_units.extend(list(self.__computer_units))  # extend

        from operator import methodcaller
        self.__all_units_sorted = sorted(all_units, key=methodcaller(sort_parameter), reverse=True)

        return

    def __add_unit(self, units_list, new_unit):

        unit_type = new_unit.get_unit_type()

        if unit_type == UNIT_TYPE_MELEE:
            units_list.insert(0, new_unit)  # Melee units are lower indexed (front line)
        elif unit_type == UNIT_TYPE_RANGE:
            units_list.append(new_unit)

        self.__sort_all_units_list()  # sort the units each time we add another one
        return

    def __remove_unit(self, units_list, unit):
        if self.__all_units_sorted[self.__current_unit] == unit:
            # if current turn's unit is the unit to remove, increment the index
            self.set_next_unit()  # ignore the return value
        units_list.remove(unit)  # remove the unit from the list
        self.__sort_all_units_list()
        return

    def add_player_unit(self, new_unit):
        self.__add_unit(self.__player_units, new_unit)

    def add_computer_unit(self, new_unit):
        self.__add_unit(self.__computer_units, new_unit)

    def remove_player_unit(self, unit):
        self.__remove_unit(self.__player_units, unit)

    def remove_computer_unit(self, unit):
        self.__remove_unit(self.__computer_units, unit)

    def get_current_unit(self):
        return self.__all_units_sorted[self.__current_unit]

    def set_next_unit(self):
        self.__current_unit += 1
        if self.__current_unit == len(self.__all_units_sorted):
            self.__current_unit = 0
        # return self.__all_units_sorted[self.__current_unit]

    def get_all_units_list(self):
        return self.__all_units_sorted

    def is_player_turn(self):
        current_unit = self.__all_units_sorted[self.__current_unit]
        return current_unit in self.__all_units_sorted
