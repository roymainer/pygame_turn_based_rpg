from Shared.Model import MODEL_TYPE_MELEE, MODEL_TYPE_RANGE


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

        unit_type = new_unit.get_model_type()

        if unit_type == MODEL_TYPE_MELEE:
            units_list.insert(0, new_unit)  # Melee units are lower indexed (front line)
        elif unit_type == MODEL_TYPE_RANGE:
            units_list.append(new_unit)

        self.__sort_all_units_list()  # sort the units each time we add another one
        return

    def add_player_unit(self, new_unit):
        self.__add_unit(self.__player_units, new_unit)

    def add_computer_unit(self, new_unit):
        self.__add_unit(self.__computer_units, new_unit)

    def get_current_unit(self):
        if self.__current_unit not in range(len(self.__all_units_sorted)):
            self.advance_to_next_unit()
        try:
            return self.__all_units_sorted[self.__current_unit]
        except:
            print("bad index!!!!")

    def advance_to_next_unit(self):
        self.__current_unit += 1
        if self.__current_unit not in range(len(self.__all_units_sorted)):
            self.__sort_all_units_list()
            self.__current_unit = 0
        # return self.__all_units_sorted[self.__current_unit]

    def get_all_units_list(self):
        return self.__all_units_sorted

    def is_player_turn(self):
        current_unit = self.__all_units_sorted[self.__current_unit]
        return current_unit in self.__all_units_sorted
    
    def get_player_unit(self, index):
        return self.__player_units[index]

    def get_all_player_units(self):
        return self.__player_units

    def get_computer_unit(self, index):
        return self.__computer_units[index]

    def get_all_computer_units(self):
        return self.__computer_units

    def remove_unit(self, unit):

        if unit in self.__player_units:
            self.__player_units.remove(unit)
        elif unit in self.__computer_units:
            self.__computer_units.remove(unit)

        if unit in self.__all_units_sorted:
            # if self.__all_units_sorted[self.__current_unit] == unit:
            #     # if current turn's unit is the unit to remove, increment the index
            #     self.set_next_unit()  # ignore the return value
            self.__all_units_sorted.remove(unit)  # remove the unit
            self.__sort_all_units_list()  # sort all units again
        return
