from player import *
import socket
import threading
import os
import tkinter as tk
import tkinter.ttk as ttk

test_character_one = Character("Dragon", 9, 3, True, True)
test_character_two = Character("Serpent", 18, 2, False, False)
test_character_three = Character("Titan", 18, 2, False, False)
test_character_four = Character("Angel", 18, 2, False, True)

list_characters_one = [test_character_one, test_character_two]
list_characters_two = [test_character_three, test_character_four]


starting_army_one = Army("wheat.png", list_characters_one, "wheat")
starting_army_two = Army("skull.png", list_characters_two, "skull")

test_opponent = Opponent("John", "Yellow")
test_opponent.add_score(10)
test_opponent.list_armies = [starting_army_one]

test_player = Player("Ian", "Black")
test_player.army_list = [starting_army_two]
test_player.add_score(747)

class MainClient(tk.Frame):
    opponents = {"John" : test_opponent} # opponent name : opponent data
    player = test_player
    my_turn = False
    turn_spot = -1

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.title("Titan Main Client")
        self.make_board()

    # tk thing that will make based off how many players it recieves
    def make_board(self):
        self.top_frame = tk.Frame(self.root)
        for opponent in self.opponents.values():
            self.make_opponent(opponent)
        self.top_frame.pack()
    # will create an opponent object with provided info and tie it into the board
    def make_opponent(self, opponent):
        OpponentFrame(self.root, opponent)

    # will make the player object to keep track of main users
    # army info and allow managing of armies wehn turn
    def make_player():
        pass

    # need to determine armies that need to be split
    # remove previously mustered units from data
    # client thing, wont be needed every time
    def upkeep():
        pass

    # go through each army and get additions if applicable
    # will need skip option if person decides not to muster, move etc.
    # client menu thing
    def muster():
        pass

    # for the purposes of this tracker
    # can denote battles occurring so fallout can be determined
    # ie points allocated units lost
    def battle():
        pass

    # triggered by button press
    # will broadcast mustered units into army on previous turn until 
    def end_turn():
        pass

    def turn(self):
        self.upkeep()
        self.muster()
        self.battle()
        self.end_turn()   

class OpponentFrame(tk.Frame):
    def __init__(self, parent, opponent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.opponent_frame = tk.Frame(self.parent)
        self.lbl_name = ttk.Label(self.opponent_frame, text=opponent.name)
        self.lbl_name.pack(side=tk.LEFT)
        self.army_frame = tk.Frame(self.opponent_frame)
        self.army_frame.pack(side=tk.LEFT)
        self.opponent_frame.pack()

if __name__ == '__main__':
    root = tk.Tk()
    MainClient(root).pack(side="top", fill="both", expand=True)
    root.mainloop()