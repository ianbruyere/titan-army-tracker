from game_data.character_data import Characters

class Player:
    score = 0
    armies = {}

    def __init__(self, name, color):
        self.name = name
        self.color = color
 
    def add_army(self, name, character_list):
        new_army = Army(name, character_list)
        new_army.set_symbol(f'./game_data/{self.color}/{new_army.name}.png') 
        self.armies[new_army.name] = new_army

    def split_army(self):
        for army in self.armies:
            if army.must_split():
                pass

    def update_army(self, army):
        self.armies[army.name] = army

    def get_score(self):
        return self.score
    
    def get_armies(self):
        return self.armies

    def add_score(self, value):
        self.score += value


class Army:
    unit_limit = 7
    character_list = []
    symbol = ''
    name = ''

    def __init__(self, name, character_list):
        self.name = name
        self.character_list = character_list

    def get_value(self):
        return sum([int(c.power) * int(c.skill) for c in self.character_list])
    
    def has_titan(self):
        return any([character.name == 'Titan' for character in self.character_list])

    def add_character(self, name):
        new_character = Characters[name]
        if self.get_num_units() < self.unit_limit:
            self.character_list.append(new_character)

    def must_split(self):
        return self.get_num_units() <=  self.unit_limit
    
    def get_num_units(self):
        return len(self.character_list)
    
    def set_symbol(self, path):
        self.symbol = path
    

# limited information    
class Opponent:
    score = 0
    name = ''
    armies = {}
    color = ''

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.armies = {} # WEIRD if I comment out this line, armies becomes shared between all opponents

    def get_score(self):
        return self.score
    
    def add_score(self, value):
        self.score += value

    def add_army(self, name, character_list):
        new_army = Army(name, character_list)
        new_army.set_symbol(f'./game_data/{self.color}/{new_army.name}.png') 
        self.armies[new_army.name] = new_army

    # reveals number of units in opponents army
    def get_armies(self):
        result = {}
        for army in self.armies.values():
            result[army.symbol] = army.get_num_units()
        return result
    
    
    