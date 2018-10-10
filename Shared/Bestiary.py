import os

from Shared.Armor import *
from Shared.Model import Model
from Shared.Shield import Shield
from Shared.Skill import *
from Shared.SpecialRule import *
from Shared.Spell import HammerOfSigmar, ShieldOfFaith, Soulfire
from Shared.Weapon import *


def get_sprite_sheet_path(file_name) -> str:
    return os.path.join("Assets", "Graphics", "Models", file_name)


# --------------------- DWARF --------------------- #
DWARF_HERO_SPRITE_SHEET = get_sprite_sheet_path("dwarf_hero_sprite_sheet.png")


def get_dwarf_hero() -> Model:
    model = Model(sprite_sheet_file=DWARF_HERO_SPRITE_SHEET,
                  # name="Dwarf Hero", m=3, ws=4, bs=3, s=3, t=4, w=1, i=2, a=2, ld=9)
                  name="Dwarf Hero", m=3, ws=6, bs=4, s=4, t=5, w=2, i=3, a=3, ld=10)  # Thane

    model.set_armor(HeavyArmor())
    model.add_weapon(Sword())

    # TODO: add special skills
    model.add_special_rule(AncestralGrudge())
    # model.add_special_rule(Relentless())  # irrelevant
    model.add_special_rule(Resolute())
    # model.add_special_rule(UndergroundAdvance())  # irrelevant
    # model.add_special_rule(MagicResistanceSR(2))
    return model


# --------------------- EMPIRE --------------------- #
EMPIRE_ARCHER_SPRITE_SHEET = get_sprite_sheet_path("archer_sprite_sheet.png")
EMPIRE_SWORDSMAN_SPRITE_SHEET = get_sprite_sheet_path("empire_swordsman_sprite_sheet.png")
WARRIOR_SPRITE_SHEET = get_sprite_sheet_path("warrior_sprite_sheet.png")
WITCH_HUNTER_SPRITE_SHEET = get_sprite_sheet_path("witch_hunter_sprite_sheet.png")
WARRIOR_PRIEST_SPRITE_SHEET = get_sprite_sheet_path("warrior_priest_sprite_sheet.png")


def get_empire_witch_hunter() -> Model:
    model = Model(sprite_sheet_file=WITCH_HUNTER_SPRITE_SHEET,
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


def get_warrior_priest() -> Model:
    model = Model(sprite_sheet_file=WARRIOR_PRIEST_SPRITE_SHEET, name="Warrior Priest",
                  m=4, ws=4, bs=4, s=4, t=4, w=2, i=4, a=2, ld=8)
    model.set_armor(HeavyArmor())
    model.add_weapon(WarHammer())

    # model.add_skill(Dispel())  # TODO: create dispel
    model.add_special_rule(RighteousFury())
    model.add_spell(HammerOfSigmar())
    model.add_spell(ShieldOfFaith())
    model.add_spell(Soulfire())
    return model


# --------------------- SKAVEN --------------------- #
SKAVEN_SLAVE_SPRITE_SHEET = get_sprite_sheet_path("skaven_slave_sprite_sheet.png")


def get_skaven_slave() -> Model:
    model = Model(sprite_sheet_file=SKAVEN_SLAVE_SPRITE_SHEET, name="Skavenslave",
                  m=5, ws=2, bs=2, s=3, t=3, w=1, i=4, a=1, ld=2)
    model.add_weapon(Spear())
    model.set_shield(Shield())
    return model


# --------------------- UNDEAD --------------------- #
UNDEAD_SKELETON_HALBERD_SPRITE_SHEET = get_sprite_sheet_path("skeleton_sprite_sheet.png")
# UNDEAD_SKELETON_HALBERD_SIZE = (50 * 2, 37 * 2)


# --------------------- MONSTERS --------------------- #
SLIME_SPRITE_SHEET = get_sprite_sheet_path("slime_sprite_sheet.png")


def get_empire_archer() -> Model:
    model = Model(sprite_sheet_file=EMPIRE_ARCHER_SPRITE_SHEET,
                  name="Empire Archer", m=4, ws=3, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)

    model.add_weapon(get_hand_weapon())
    model.add_weapon(Bow())

    return model


def get_warrior() -> Model:
    return Model(sprite_sheet_file=EMPIRE_SWORDSMAN_SPRITE_SHEET,
                 name="Warrior", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)


def get_empire_swordsman() -> Model:
    model = Model(sprite_sheet_file=EMPIRE_SWORDSMAN_SPRITE_SHEET,
                  name="Empire Swordsman", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)

    model.set_armor(LightArmor())
    model.add_weapon(Sword())
    model.set_shield(Shield())

    return model


def get_undead_skeleton_halberd() -> Model:
    model = Model(sprite_sheet_file=UNDEAD_SKELETON_HALBERD_SPRITE_SHEET,
                  name="Undead Halberd", m=4, ws=2, bs=2, s=3, t=3, w=1, i=2, a=1, ld=3)

    model.add_weapon(Halberd())
    model.set_armor(LightArmor())
    model.set_shield(Shield())

    model.add_special_rules(Undead())

    return model


def get_slime_monster() -> Model:
    return Model(sprite_sheet_file=SLIME_SPRITE_SHEET, name="Slime", m=4, ws=4, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7)
