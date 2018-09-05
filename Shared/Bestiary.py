import os
from Shared.Armor import *
from Shared.Shield import Shield
from Shared.Spell import HammerOfSigmar, ShieldOfFaith, Soulfire
from Shared.Weapon import *
from Shared.ModelFF import ModelFF
from Shared.Skill import *
from Shared.SpecialRule import *


def get_sprite_sheet_path(file_name) -> str:
    return os.path.join("Assets", "Graphics", "Models", file_name)


# --------------------- EMPIRE --------------------- #
EMPIRE_ARCHER_SPRITE_SHEET = get_sprite_sheet_path("archer_sprite_sheet.png")
# EMPIRE_ARCHER_SIZE = (50 * 3, 37 * 3)
EMPIRE_SWORDSMAN_SPRITE_SHEET = get_sprite_sheet_path("empire_swordsman_sprite_sheet.png")
# EMPIRE_SWORDSMAN_SIZE = (int(36 * 1.5), int(48 * 1.5))
# EMPIRE_SWORDSMAN_SIZE = None
WARRIOR_SPRITE_SHEET = get_sprite_sheet_path("warrior_sprite_sheet.png")
# WARRIOR_SIZE = (50 * 3, 37 * 3)
WITCH_HUNTER_SPRITE_SHEET = get_sprite_sheet_path("witch_hunter_sprite_sheet.png")
WARRIOR_PRIEST_SPRITE_SHEET = get_sprite_sheet_path("warrior_priest_sprite_sheet.png")
DWARF_HERO_SPRITE_SHEET = get_sprite_sheet_path("dwarf_hero_sprite_sheet.png")


# --------------------- UNDEAD --------------------- #
UNDEAD_SKELETON_HALBERD_SPRITE_SHEET = get_sprite_sheet_path("skeleton_sprite_sheet.png")
# UNDEAD_SKELETON_HALBERD_SIZE = (50 * 2, 37 * 2)

# --------------------- MONSTERS --------------------- #
SLIME_SPRITE_SHEET = get_sprite_sheet_path("slime_sprite_sheet.png")


# SLIME_SIZE = (100 * 1, 74 * 1)


def get_empire_archer() -> ModelFF:
    model = ModelFF(sprite_sheet_file=EMPIRE_ARCHER_SPRITE_SHEET,
                    name="Empire Archer", m=4, ws=3, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)

    model.add_weapon(get_hand_weapon())
    model.add_weapon(Bow())

    return model


def get_warrior() -> ModelFF:
    return ModelFF(sprite_sheet_file=EMPIRE_SWORDSMAN_SPRITE_SHEET,
                   name="Warrior", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)


def get_empire_swordsman() -> ModelFF:
    model = ModelFF(sprite_sheet_file=EMPIRE_SWORDSMAN_SPRITE_SHEET,
                    name="Empire Swordsman", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)

    model.set_armor(LightArmor())
    model.add_weapon(Sword())
    model.set_shield(Shield())

    return model


def get_empire_witch_hunter() -> ModelFF:
    model = ModelFF(sprite_sheet_file=WITCH_HUNTER_SPRITE_SHEET,
                    name="Witch Hunter", m=4, ws=4, bs=4, s=4, t=4, w=2, i=4, a=2, ld=8)

    model.set_armor(LightArmor())
    model.add_weapon(get_hand_weapon())
    model.add_weapon(Pistol())

    model.add_skill(AccusationSkill())
    # model.add_skill(SniperSkill())  # not sure if it's relevant
    model.add_special_rule(GrimResolveSR())
    model.add_special_rule(ToolsOfJudgmentSR())
    # TODO: model.add_special_rule(MagicResistanceSR(2))

    return model


def get_warrior_priest() -> ModelFF:
    model = ModelFF(sprite_sheet_file=WARRIOR_PRIEST_SPRITE_SHEET, name="Warrior Priest",
                    m=4, ws=4, bs=4, s=4, t=4, w=2, i=4, a=2, ld=8)
    model.set_armor(HeavyArmor())
    model.add_weapon(WarHammer())

    # model.add_skill(Dispel())  # TODO: create dispel
    model.add_special_rule(RighteousFury())
    model.add_spell(HammerOfSigmar())
    model.add_spell(ShieldOfFaith())
    model.add_spell(Soulfire())

    return model


def get_dwarf_hero() -> ModelFF:
    model = ModelFF(sprite_sheet_file=DWARF_HERO_SPRITE_SHEET,
                    name="Dwarf Hero", m=3, ws=4, bs=3, s=3, t=4, w=1, i=2, a=2, ld=9)
                    # name="Dwarf Hero", m=3, ws=1, bs=3, s=3, t=4, w=9, i=2, a=2, ld=9)

    model.set_armor(HeavyArmor())
    model.add_weapon(Sword())

    # TODO: add special skills
    model.add_special_rule(AncestralGrudge())
    # model.add_special_rule(Relentless())  # irrelevant
    model.add_special_rule(Resolute())
    # model.add_special_rule(UndergroundAdvance())  # irrelevant
    # model.add_special_rule(MagicResistanceSR(2))

    return model


def get_undead_skeleton_halberd() -> ModelFF:
    model = ModelFF(sprite_sheet_file=UNDEAD_SKELETON_HALBERD_SPRITE_SHEET,
                    name="Undead Halberd", m=4, ws=2, bs=2, s=3, t=3, w=1, i=2, a=1, ld=3)

    model.add_weapon(Halberd())
    model.set_armor(LightArmor())
    model.set_shield(Shield())

    model.add_special_rules(Undead())

    return model


def get_slime_monster() -> ModelFF:
    return ModelFF(sprite_sheet_file=SLIME_SPRITE_SHEET, name="Slime", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)
