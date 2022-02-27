from collections import namedtuple
import csv

Character = namedtuple('Creature', ('type', 'name', 'power', 'skill', 'range_strength', 'can_fly', 'ruleset'))
# JMB suggested I make the Character name the color of the tile for 
# would implement that here in the future, or we could use minified unit tiles

# I also want to do filtering at some point of lineage
# so the only things you can muster from an area are ones you have the lineage for
# kind of rudimentary "knowing" what space the person is on without actually implementing that feature
with open("./game_data/characters.csv", 'r') as f:
    r = csv.reader(f)
    next(r) # skipping header
    Characters = {Character(*i).name: Character(*i) for i in r}