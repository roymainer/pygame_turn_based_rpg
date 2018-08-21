from Armory.Armor import *


NONE = {NAME: "None", ARMOR_RATING: 0, WS: 0, BS: 0, S: 0, T: 0, W: 0, I: 0, A: 0, LD: 0, TO_HIT_RE_ROLL: 0}
SHIELD = {NAME: "Shield", ARMOR_RATING: -1, WS: 0, BS: 0, S: 0, T: 0, W: 0, I: 0, A: 0, LD: 0, TO_HIT_RE_ROLL: 0}


class Shield(Armor):
    
    def __init__(self, attributes):
        super(Shield, self).__init__(attributes)
