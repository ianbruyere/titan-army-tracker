from enum import auto
import os

class Teams(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    BROWN = 5
    BLACK = 6

class Color:
    color = ''
    army_names = []
    def get_path_images(self):
        return os.path(f'./{self.color}/')

class Black(Color):
    color = 'black'
    SKULL = auto()
    HEADSTONE = auto()
    SPIKE_CUBE = auto()
    SUN_EYE = auto()
    DUAL_HALBERD = auto()
    HAND = auto()
    PUMPKIN = auto()
    FEATHER = auto()
    ROSE = auto()
    SCORPION = auto()
    ARROWHEAD = auto()
    BOLT = auto()

class Yellow(Color):
    color = 'black'
    armies = {
        'ARMS' : './yellow/arms.png',
        'CLAW' : './yellow/claw.png',
        'COINS' : './yellow/coins.png'
        # CROWN = auto()
        # HORN = auto()
        # ILLUMINATI = auto()
        # LAMP = auto()
        # RINGS = auto()
        # SCARAB = auto()
        # SNAKE = auto()
        # SUN = auto()
        # WHEAT = auto()
    }
