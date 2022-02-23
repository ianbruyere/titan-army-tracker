class Character:
    def __init__(self, name, power, skill, can_range, can_fly):
        self.name = name
        self.power = power
        self.skill = skill
        self.can_range = can_range
        self.can_fly = can_fly

    def get_name(self):
        return self.name
    
    def get_value(self):
        return self.skill * self.power
    

class Army:
    unit_limit = 7
    character_list = []
    name = ''

    def __init__(self, name, character_list, symbol):
        self.name = name
        self.character_list = character_list
        self.symbol = symbol

    def get_value(self):
        return sum([character.get_value() for character in self.character_list])
    
    def has_titan(self):
        return any([character.name == 'Titan' for character in self.character_list])

    def add_character(self, name, power, skill, can_range, can_fly):
        new_character = Character(name, power,skill, can_range, can_fly)
        if not self.must_split:
            self.character_list.append(new_character)

    def must_split(self):
        return self.get_num_units <= 7
    
    def get_num_units(self):
        return len(self.character_list)
        
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.army_list = []
        self.score = 0

    def add_army(self, name, character_list, symbol):
        new_army = Army(name, character_list, symbol)
        self.army_list.append(new_army)

    def split_army(self):
        for army in self.army_list:
            if army.must_split():
                pass

    def get_score(self):
        return self.score
    
    def add_score(self, value):
        self.score += value
    
class Opponent:
    score = 0
    name = 0
    list_armies = []
    color = ''

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.army_list = []
        self.score = 0

    def get_score(self):
        return self.score
    
    def add_score(self, value):
        self.score += value

    # reveals number of units in opponents army
    def get_armies(self):
        result = {}
        for army in self.list_armies:
            result[army.symbol] = army.get_num_units()
        return result
    
    
    