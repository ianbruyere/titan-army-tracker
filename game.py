from player import *
import socket
import threading
import os
import tkinter as tk
import tkinter.ttk as ttk

######## TESTING DATA ############
test_character_one = Character("Dragon", 9, 3, True, True)
test_character_two = Character("Serpent", 18, 2, False, False)
test_character_three = Character("Titan", 18, 2, False, False)
test_character_four = Character("Angel", 18, 2, False, True)

list_characters_one = [test_character_one, test_character_two]
list_characters_two = [test_character_three, test_character_four]
list_characters_three = [test_character_one, test_character_three, test_character_four]


starting_army_one = Army("wheat.png", list_characters_one, "./game_data/Yellow/wheat.png")
starting_army_two = Army("skull.png", list_characters_two, "./game_data/Black/skull.png")
starting_army_four = Army("skull.png", list_characters_two, "./game_data/Black/b_eye.png")
starting_army_three = Army("wheat.png", list_characters_three, "./game_data/Yellow/sun.png")


test_opponent = Opponent("John", "Yellow")
test_opponent.add_score(10)
test_opponent.list_armies = [starting_army_one, starting_army_three]

test_opponent_two = Opponent("Cash", "Black")
test_opponent_two.list_armies = [starting_army_four]

test_player = Player("Ian", "Black")
test_player.army_list = [starting_army_two]
test_player.add_score(747)

############## END TESTING DATA ######################



class MainClient(tk.Frame):
    opponents = {"John" : test_opponent, "Cash": test_opponent_two} # opponent name : opponent data
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
        self.make_player()

    # will create an opponent object with provided info and tie it into the board
    def make_opponent(self, opponent):
        new_frame = OpponentFrame(self.root, opponent)
        new_frame.pack()

    # will make the player object to keep track of main users
    # army info and allow managing of armies wehn turn
    def make_player(self):
        self.player_frame = tk.Frame(self.root)
        
        self.lbl_name = ttk.Label(self.player_frame, text = self.player.name, font=("Times New Roman", 24))
        self.lbl_score = ttk.Label(self.player_frame, text = self.player.score, font=("Times New Roman", 24), foreground="green")
        self.lbl_name.pack(side=tk.LEFT)
        self.lbl_score.pack(side=tk.LEFT)
        
        for army in self.player.army_list:
            new_frame = PlayerArmyFrame(self.player_frame, army)
            new_frame.pack()
        
        self.player_frame.pack()


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
        self.opponent_frame = tk.Frame(self.parent, highlightbackground=opponent.color, highlightthickness=2)

        self.lbl_name = ttk.Label(self.opponent_frame, text=opponent.name, font=("Times New Roman", 24))
        self.lbl_score = ttk.Label(self.opponent_frame, text=opponent.get_score(), font=("Times New Roman", 24), foreground="green")

        self.lbl_name.pack(side=tk.LEFT)
        self.lbl_score.pack(side=tk.LEFT)
        # frame for armies
        self.armies_frame = tk.Frame(self.opponent_frame)
        # TODO make a scrollbar
        # TODO make an initial fixed size that will hold 2 armies expand up to 3, then horizontal scroll
        # make each army
        for symbol, num_units in opponent.get_armies().items():
            new_frame = OpponentArmyFrame(self.armies_frame, symbol, num_units)
            new_frame.pack(side=tk.LEFT)

        self.armies_frame.pack(side=tk.BOTTOM, pady=(5, 10))
        self.opponent_frame.pack()

class OpponentArmyFrame(tk.Frame):
    image = ''
    def __init__(self, parent, symbol, num_units, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.image = tk.PhotoImage(file=symbol)
        self.parent = parent
        self.army_frame = tk.Frame(self.parent)
        self.lbl_army = ttk.Label(self.army_frame, image=self.image)
        self.lbl_units = ttk.Label(self.army_frame, text = str(num_units), font=("Times New Roman", 24))
        self.lbl_army.pack()
        self.lbl_units.pack()
        self.army_frame.pack(side=tk.LEFT)

class PlayerArmyFrame(tk.Frame):
    image = ''
    army = None

    def __init__(self, parent, army, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.image = tk.PhotoImage(file=army.symbol)
        self.army = army
        self.parent = parent
        self.army_frame = tk.Frame(self.parent)

        self.lbl_army = ttk.Label(self.army_frame, image=self.image)
        self.lbl_army.bind("<Button-1>", lambda e : self.open_menu(e))
        self.lbl_units = ttk.Label(self.army_frame, text=str(army.get_num_units()), font=("Times New Roman", 24))
        self.lbl_value = ttk.Label(self.army_frame, text=str(army.get_value()), font=("Times New Roman", 24), foreground = "cyan")

        self.lbl_army.pack()
        self.lbl_units.pack(side=tk.LEFT)
        self.lbl_value.pack(side=tk.RIGHT)
        self.army_frame.pack(side=tk.LEFT)

    def open_menu(self, event):
        window = PlayerArmyMenu(self.parent, self.army)

class PlayerArmyMenu:
    def __init__(self, parent, army, *args, **kwargs):
        self.top = tk.Toplevel(parent)
        self.top.geometry("200x200")
        self.top.title(army.name)
        for character in army.character_list:
            n_w = CharacterMenuItem(self.top, character)



class CharacterMenuItem(tk.Frame):
    def __init__(self, parent, character, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.character_frame = tk.Frame(self.parent)

        self.lbl_character = ttk.Label(self.character_frame, text=character.get_name())
        self.lbl_character.pack()
        self.character_frame.pack()


if __name__ == '__main__':
    root = tk.Tk()
    MainClient(root).pack(side="top", fill="both", expand=True)
    root.mainloop()