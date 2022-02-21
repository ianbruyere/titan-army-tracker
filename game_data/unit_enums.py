from enum import auto, Flag

class Creatures(Flag):
    BEHEMOTH = auto()
    CENTAUR = auto()
    COLOSSUS = auto()
    CYCLOPS = auto()
    DRAGON = auto()
    GARGOYLE = auto()
    GIANT = auto()
    GORGON = auto()
    GRIFFON = auto()
    LION = auto()
    MINOTAUR = auto()
    OGRE = auto()
    RANGER = auto()
    SERPENT = auto()
    TROLL = auto()
    UNICORN = auto()
    WARBEAR = auto()
    WYVERN = auto()

class DemiLords(Flag):
    GUARDIANS = auto()
    WARLOCK = auto

class Lords(Flag):
    ANGEL = auto()
    ARCHANGEL = auto()
    TITAN = auto()