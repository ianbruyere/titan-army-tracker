from collections import namedtuple
import csv

Character = namedtuple('Creature', ('type', 'name', 'power', 'skill', 'range_strength', 'can_fly', 'ruleset'))

with open("./game_data/characters.csv", 'r') as f:
    r = csv.reader(f)
    next(r) # skipping header
    Characters = {Character(*i).name: Character(*i) for i in r}