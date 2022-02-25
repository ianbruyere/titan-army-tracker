from faulthandler import disable
from typing import overload
from player import *
from game_data.character_data import Characters
import socket
import threading
import os
import tkinter as tk
import tkinter.ttk as ttk

BIG_FONT = ("Times New Roman", 24)
FONT = ("Times New Roman", 16)
######## TESTING DATA ############
test_character_one = Characters["Dragon"]
test_character_two = Characters["Serpent"]
test_character_three = Characters["Titan"]
test_character_four = Characters["Angel"]

list_characters_one = [test_character_one]
list_characters_two = [test_character_one, test_character_two, test_character_three]
list_characters_three = [test_character_one, test_character_two, test_character_three]
list_characters_four = [test_character_one, test_character_two, test_character_three, test_character_four]

test_opponent_one = Opponent("John", "Yellow")
test_opponent_one.add_army("wheat", list_characters_one)
test_opponent_one.add_army("arms", list_characters_two)
test_opponent_one.add_score(10)
# print(f"test opponent one: {test_opponent_one.armies}")

test_opponent_two = Opponent("Cash", "Black")
test_opponent_two.add_army("eye", list_characters_four)
# print(f"test opponent two: {test_opponent_two.armies}")

test_player = Player("Ian", "Black")
test_player.add_army("skull", list_characters_one)
test_player.add_army("scorpion", list_characters_four)
test_player.add_score(747)

############## END TESTING DATA ######################


class MainClient(tk.Frame):
    opponents = {"John" : test_opponent_one, "Cash": test_opponent_two} # opponent name : opponent data
    #player = test_player
    my_turn = False
    turn_number = -1
    army_frames = {}

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.root = parent
        self.root.title("Titan Main Client")
        self.player = test_player
        self.make_board()

    def get_player(self):
        return self.player

    # tk thing that will make based off how many players it recieves
    def make_board(self):
        self.make_opponents()
        self.init_player()

    # will create an opponent object with provided info and tie it into the board
    def make_opponents(self):
        for opponent in self.opponents.values():
            opponent_frame = OpponentFrame(self.root, opponent)
            opponent_frame.pack()

    # will make the player object to keep track of main users
    # army info and allow managing of armies wehn turn
    def init_player(self):
        self.player_frame = tk.Frame(self.root)
        
        self.lbl_name = ttk.Label(self.player_frame, text = self.player.name, font=BIG_FONT)
        self.lbl_score = ttk.Label(self.player_frame, text = self.player.score, font=BIG_FONT, foreground="green")
        self.lbl_name.pack(side=tk.LEFT)
        self.lbl_score.pack(side=tk.LEFT)
        
        for army in self.get_player().get_armies().values():
            new_frame = PlayerArmyFrame(self.player_frame, army, self.get_player())
            self.army_frames[army.name] = new_frame
            new_frame.pack()
        
        self.player_frame.pack()
    
    


# contains information about player armies, score
class PlayerArmyFrame(tk.Frame):
    image = ''
    army = None

    def __init__(self, parent, army, player, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.image = tk.PhotoImage(file=army.symbol)
        self.army = army
        self.parent = parent
        self.army_frame = tk.Frame(self.parent)

        self.army_value = tk.StringVar()
        self.army_num = tk.StringVar()
        self.army_value.set(str(army.get_value()))
        self.army_num.set(str(army.get_num_units()))
        self.army_num.trace("w", self.update)
        self.army_value.trace("w", self.update)

        self.lbl_army = ttk.Label(self.army_frame, image=self.image)
        self.lbl_army.bind("<Button-1>", lambda e : self.open_menu(e, army, player))
        self.lbl_units = ttk.Label(self.army_frame, text=self.army_num.get(), font=BIG_FONT)
        self.lbl_value = ttk.Label(self.army_frame, text=self.army_value.get(), font=BIG_FONT, foreground = "cyan")


        self.lbl_army.pack()
        self.lbl_units.pack(side=tk.LEFT)
        self.lbl_value.pack(side=tk.RIGHT)
        self.army_frame.pack(side=tk.LEFT)

    def open_menu(self, event, army, player):
        window = PlayerArmyMenu(self, self.army, player)

    def update(self, *args):
        self.lbl_units['text'] = self.army.get_num_units()
        self.lbl_value['text'] = self.army.get_value()


# TODO
# refactor into:
# Base State
# muster state
# upkeep(split) state
# resolve conflict state
# so there can be a forced flow for turn
# and a clear delineation when it's your turn vs someone elses
# but this works for first pass

# in-depth information about the players armies
class PlayerArmyMenu(tk.Toplevel):
    image = ''
    army = None
    c_list = []

    def __init__(self, parent, army, player, *args, **kwargs):
        self.image = tk.PhotoImage(file=army.symbol)
        tk.Toplevel.__init__(self)
        self.title(army.name)
        self.parent=parent
        # army info
        self.current_army_frame = tk.Frame(self)
        self.lbl_current_army = ttk.Label(self.current_army_frame, text = "Current Army")
        self.lbl_current_army_image = ttk.Label(self.current_army_frame, image=self.image, text = "WHY NO SHOW UP")
        self.lbl_current_army_value = ttk.Label(self.current_army_frame, text = str(army.get_value()), foreground="cyan")
        # pack army info
        self.lbl_current_army.pack()
        self.lbl_current_army_image.pack()
        self.lbl_current_army_value.pack()

        for c in army.character_list:
            character_item = CharacterMenuItem(self.current_army_frame, c.name)
            character_item.pack()
            self.c_list.append(character_item)

        # Buttons
        self.split_button = tk.Button(self.current_army_frame, text='Split', command=lambda : self.split_army(army))
        self.split_button.pack(side=tk.LEFT)
        self.muster_button = tk.Button(self.current_army_frame, text='Muster', command=lambda: self.muster_unit(army,player, parent))
        self.muster_button.pack(side=tk.LEFT)
        self.current_army_frame.pack(side=tk.LEFT)

    def muster_unit(self, army, player, parent):
        self.muster_frame = tk.Frame(self.current_army_frame)
        self.split_button.pack_forget()
        self.muster_button.pack_forget()
        # makes the stuff
        self.lbl_mustering = ttk.Label(self.muster_frame, text="You are Mustering", foreground='yellow', font=FONT)
        self.new_unit_select = tk.StringVar(self.muster_frame)
        self.characters = tk.OptionMenu(self.muster_frame, self.new_unit_select, *[c for c in Characters.keys()])
        self.save_button = tk.Button(self.muster_frame, text="Save", command=lambda : self.save_muster_unit(army, player, parent))
        # sub units pack
        self.lbl_mustering.pack()
        self.characters.pack()
        self.save_button.pack()
        # main local frame
        self.muster_frame.pack(side=tk.LEFT)

    # TODO doesnt update unit list until refresh
    # save selected unit to army
    def save_muster_unit(self, army, player, parent):
        # update objects
        if self.new_unit_select.get(): army.add_character(self.new_unit_select.get())
        player.update_army(army)
        # update interface
        c = CharacterMenuItem(self.current_army_frame, self.new_unit_select.get()).pack()
        self.lbl_current_army_value['text'] = army.get_value()
        self.c_list.append(c)
        # return UI to original state
        self.muster_frame.destroy()
        self.split_button.pack()
        self.muster_button.pack()
        self.parent.army_num.set(100)

    def split_army(self):
        pass


    
# to display information about characters in an army
class CharacterMenuItem(tk.Frame):
    def __init__(self, parent, character, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.character_frame = tk.Frame(self.parent)

        self.lbl_character = ttk.Label(self.character_frame, text=character)
        self.lbl_character.pack()
        self.character_frame.pack()



class OpponentFrame(tk.Frame):

    def __init__(self, parent, opponent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.opponent_frame = tk.Frame(self.parent, highlightbackground=opponent.color, highlightthickness=2)

        self.lbl_name = ttk.Label(self.opponent_frame, text=opponent.name, font=BIG_FONT)
        self.lbl_score = ttk.Label(self.opponent_frame, text=opponent.get_score(), font=BIG_FONT, foreground="green")

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


# info about opponents as the game allows: # of units, score
class OpponentArmyFrame(tk.Frame):
    image_army = ''
    last_mustered_unit='' # TODO game client sends last updated unit, on hover will show per army

    def __init__(self, parent, symbol, num_units, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.image_army = tk.PhotoImage(file=symbol)

        self.parent = parent
        self.army_frame = tk.Frame(self.parent)

        self.lbl_army = ttk.Label(self.army_frame, image=self.image_army)
        self.lbl_units = ttk.Label(self.army_frame, text = str(num_units), font=BIG_FONT)

        self.lbl_army.pack()
        self.lbl_units.pack()
        # main frame pack
        self.army_frame.pack(side=tk.LEFT)



if __name__ == '__main__':
    root = tk.Tk()
    MainClient(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


    # def open_menu(self, event, army, player):
    #     self.window = PlayerArmyMenu(self.root, army, player)
    #     #self.window.protocol("WM_DELETE_WINDOW", self.on_destroy)

    # # need to determine armies that need to be split
    # # remove previously mustered units from data
    # # client thing, wont be needed every time
    # def upkeep():
    #     pass

    # # go through each army and get additions if applicable
    # # will need skip option if person decides not to muster, move etc.
    # # client menu thing
    # def muster():
    #     pass

    # # for the purposes of this tracker
    # # can denote battles occurring so fallout can be determined
    # # ie points allocated units lost
    # def battle():
    #     pass

    # # triggered by button press
    # # will broadcast mustered units into army on previous turn until 
    # def end_turn():
    #     pass

    # def turn(self):
    #     self.upkeep()
    #     self.muster()
    #     self.battle()
    #     self.end_turn()   
