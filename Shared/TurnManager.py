import operator

from Shared.CharacterConstatns import CharacterConstants


class TurnManager:

    def __init__(self):
        self.__player_units = []  # used to keep player units in formation
        self.__computer_units = []  # used to keep computer units in formation
        self.__all_units_sorted = []  # all units sorted by initiative
        self.__next_unit = None  # index to next turn's unit

    def __sort_all_units_list(self, sort_parameter: str= 'initiative'):
        # copy and merge both units lists
        all_units = list(self.__player_units)
        all_units.extend(list(self.__computer_units))

        all_units.sort(key=operator.attrgetter(sort_parameter))  # sort by parameter 'initiative'
        self.__all_units_sorted = all_units  # update the all units list
        return

    def __add_unit(self, units_list, new_unit):

        unit_type = new_unit.get_unit_type()

        if unit_type == CharacterConstants.UNIT_TYPE_MELEE:
            index_array = range(3)  # melee units are indexed 0-2
        elif unit_type == CharacterConstants.UNIT_TYPE_RANGE:
            index_array = range(3, 6)  # ranged units are indexed 3-5

        for i in index_array:
            if units_list[i] is None:
                units_list[i] = new_unit

        self.__sort_all_units_list()  # sort the units each time we add another one
        return

    def __remove_unit(self, units_list, unit):
        unit_index = units_list.index(unit)  # get the unit
        if self.__all_units_sorted[self.__next_unit] == unit:
            # if next turn's unit is the unit to remove, increment the index
            self.__get_next_unit()  # ignore the return value
        self.units_list[unit_index] = None  # remove the unit from the list
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
        
    def get_next_unit(self):
        self.__next_unit += 1
        if self.__next_unit == len(self.__all_units_sorted):
            self.__next_unit = 0

        return self.__all_units_sorted[self.__next_unit]

    def get_all_units_list(self):
        return self.__all_units_sorted



