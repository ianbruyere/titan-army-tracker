from faulthandler import disable
from player import *
from game_data.character_data import Characters
import socket
import threading
import os
import tkinter as tk
import tkinter.ttk as ttk

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

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.title("Titan Main Client")
        self.player = test_player
        self.make_board()

    # tk thing that will make based off how many players it recieves
    def make_board(self):
        self.make_opponents()
        self.make_player()

    # will create an opponent object with provided info and tie it into the board
    def make_opponents(self):
        for opponent in self.opponents.values():
            opponent_frame = OpponentFrame(self.root, opponent)
            opponent_frame.pack()

    # will make the player object to keep track of main users
    # army info and allow managing of armies wehn turn
    def make_player(self):
        self.player_frame = tk.Frame(self.root)
        
        self.lbl_name = ttk.Label(self.player_frame, text = self.player.name, font=("Times New Roman", 24))
        self.lbl_score = ttk.Label(self.player_frame, text = self.player.score, font=("Times New Roman", 24), foreground="green")
        self.lbl_name.pack(side=tk.LEFT)
        self.lbl_score.pack(side=tk.LEFT)
        
        for army in self.player.armies.values():
            new_frame = PlayerArmyFrame(self.player_frame, army, self.player)
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
        self.lbl_units = ttk.Label(self.army_frame, text = str(num_units), font=("Times New Roman", 24))

        self.lbl_army.pack()
        self.lbl_units.pack()
        # main frame pack
        self.army_frame.pack(side=tk.LEFT)

# contains information about player armies, score
class PlayerArmyFrame(tk.Frame):
    image = ''
    army = None

    def __init__(self, parent, army, player, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.image = tk.PhotoImage(file=army.symbol)
        # self.army = army
        self.parent = parent
        self.army_frame = tk.Frame(self.parent)

        self.lbl_army = ttk.Label(self.army_frame, image=self.image)
        self.lbl_army.bind("<Button-1>", lambda e : self.open_menu(e, army, player))
        self.lbl_units = ttk.Label(self.army_frame, text=str(army.get_num_units()), font=("Times New Roman", 24))
        self.lbl_value = ttk.Label(self.army_frame, text=str(army.get_value()), font=("Times New Roman", 24), foreground = "cyan")

        self.lbl_army.pack()
        self.lbl_units.pack(side=tk.LEFT)
        self.lbl_value.pack(side=tk.RIGHT)
        self.army_frame.pack(side=tk.LEFT)

    def open_menu(self, event, army, player):
        window = PlayerArmyMenu(self.parent, army, player)
        # window.pack()


# in-depth information about the players armies
# TODO
# refactor into a muster state
# upkeep(split) state
# remove/resolve conflict state
# end turn when all is done for each army
# but this works for first pass
class PlayerArmyMenu:
    image = ''
    army = None
    def __init__(self, parent, army, player, *args, **kwargs):
        self.image = tk.PhotoImage(file=army.symbol)

        self.top = tk.Toplevel(parent)
        self.top.geometry("250x300")
        self.top.title(army.name)
        # army info
        self.current_army_frame = tk.Frame(self.top)
        self.lbl_current_army = ttk.Label(self.current_army_frame, text = "Current Army")
        self.lbl_current_army_image = ttk.Label(self.current_army_frame, image=self.image, text = "WHY NO SHOW UP")
        self.lbl_current_army_value = ttk.Label(self.current_army_frame, text = str(army.get_value()), foreground="cyan")
        # pack army info
        self.lbl_current_army.pack()
        self.lbl_current_army_image.pack()
        self.lbl_current_army_value.pack()
        # get units in army
        for character in army.character_list:
            n_w = CharacterArmyMenuItem(self.current_army_frame, character)
            n_w.pack()

        # Buttons
        self.split_button = tk.Button(self.current_army_frame, text='Split', command=lambda : self.split_army(army))
        self.split_button.pack(side=tk.LEFT)
        self.muster_button = tk.Button(self.current_army_frame, text='Muster', command=lambda: self.muster_unit(army,player))
        self.muster_button.pack(side=tk.LEFT)
        self.current_army_frame.pack(side=tk.LEFT)
    
    def split_army(self, army):
        pass

    def muster_unit(self, army, player):
        self.muster_frame = tk.Frame(self.current_army_frame)
        self.split_button.pack_forget()
        # makes the stuff
        self.lbl_mustering = ttk.Label(self.muster_frame, text="You are Currently Mustering", font=("Times New Roman", 16))
        self.new_unit_select = tk.StringVar(self.muster_frame)
        self.characters = tk.OptionMenu(self.muster_frame, self.new_unit_select, *[c for c in Characters.keys()])
        self.save_button = tk.Button(self.muster_frame, text="Save", command=lambda : self.save_muster_unit(army, player))
        # sub units pack
        self.lbl_mustering.pack()
        self.characters.pack()
        self.save_button.pack()
        # main local frame
        self.muster_frame.pack(side=tk.LEFT)

    def save_muster_unit(self, army, player):
        # save selected unit to army
        #TODO need to refactor Creature Enum and Character Class
        # to simply be dictionary w/ tuples
        army.add_character(self.new_unit_select.get())
        player.update_army(army)
        self.muster_frame.destroy()
        self.split_button.pack()

# to display information about characters in an army
class CharacterArmyMenuItem(tk.Frame):
    def __init__(self, parent, character, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.character_frame = tk.Frame(self.parent)

        self.lbl_character = ttk.Label(self.character_frame, text=character.name)
        self.lbl_character.pack()
        self.character_frame.pack()

# class CharacterDropDown:
#     def __init__(self, parent, menu_select *args, **kwargs):
#         self.root = tk.OptionMenu(parent, menu_select, *[c.name for c in Creatures])





if __name__ == '__main__':
    root = tk.Tk()
    MainClient(root).pack(side="top", fill="both", expand=True)
    root.mainloop()