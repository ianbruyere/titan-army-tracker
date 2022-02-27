from faulthandler import disable
from typing import overload
from player import *
from opponent import *
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

test_player = Player("Ian", "Green")
test_player.add_army("g_fish", list_characters_one)
test_player.add_army("g_snake", list_characters_four)
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
            new_frame = PlayerOverview(self, army, self.get_player())
            self.army_frames[army.name] = new_frame
            new_frame.pack()
            
        self.army_tracker = tk.StringVar()
        self.army_tracker.set(self.army_frames)
        self.army_tracker.trace('w', self.update_army_frames)
        self.player_frame.pack(side=tk.LEFT)

    def update_army_frames(self):
        for army_frame in self.army_frames:
            army_frame.update()
    # need to determine armies that need to be split
    # remove previously mustered units from data
    # client thing, wont be needed every time
    def upkeep(self):
        pass

    # go through each army and get additions if applicable
    # will need skip option if person decides not to muster, move etc.
    # client menu thing
    def muster(self):
        pass

    # for the purposes of this tracker
    # can denote battles occurring so fallout can be determined
    # ie points allocated units lost
    def battle(self):
        pass

    # triggered by button press
    # will broadcast mustered units into army on previous turn until 
    def end_turn(self):
        pass

    def turn(self):
        self.upkeep()
        self.muster()
        self.battle()
        self.end_turn()   

    
    


# contains information about player armies, score
class PlayerOverview(tk.Frame):
    image = ''
    army = None
    my_turn = False
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
        self.army_num.trace("w", self.update_lbls)
        self.army_value.trace("w", self.update_lbls)

        self.lbl_army = ttk.Label(self.army_frame, image=self.image)
        self.lbl_army.bind("<Button-1>", lambda e : self.open_menu(e, player))
        self.lbl_units = ttk.Label(self.army_frame, text=self.army_num.get(), font=BIG_FONT)
        self.lbl_value = ttk.Label(self.army_frame, text=self.army_value.get(), font=BIG_FONT, foreground = "cyan")


        self.lbl_army.pack()
        self.lbl_units.pack(side=tk.LEFT)
        self.lbl_value.pack(side=tk.RIGHT)
        self.army_frame.pack(side=tk.LEFT)

    def open_menu(self, event, player):
        PlayerArmyBaseMenu(self, self.army, player)

    def update_frames(self):
        pass
    def update_lbls(self, *args):
        self.lbl_units['text'] = self.army.get_num_units()
        self.lbl_value['text'] = self.army.get_value()
        # for army_frame in self.parent.army_frames:
        #     if not int(army_frame.army.get_num_units()):
        #         self.parent.army_frames[army_frame.name].pop()
        #         break


# TODO
# refactor into:
# Base State
# muster state
# upkeep(split) state
# resolve conflict state
# so there can be a forced flow for turn
# and a clear delineation when it's your turn vs someone elses
# but this works for first pass
class PlayerArmyBaseMenu(tk.Toplevel):
    image = ''
    army = None
    player = None
    symbol = ''
    c_frames = []
    btn_frames = []

    def __init__(self, parent, army, player, *args, **kwargs):
        self.c_frames = []
        self.image = tk.PhotoImage(file=army.symbol)
        self.army = army
        self.player = player
        tk.Toplevel.__init__(self)
        self.title(army.name)
        self.parent = parent
        # army info
        self.army_frame = tk.Frame(self)
        self.lbl_current_army = ttk.Label(self.army_frame, text = "Current Army")
        self.lbl_current_army_image = ttk.Label(self.army_frame, image=self.image, text = "WHY NO SHOW UP")
        self.lbl_current_army_value = ttk.Label(self.army_frame, text = str(army.get_value()), foreground="cyan")
        # pack army info
        self.lbl_current_army.pack()
        self.lbl_current_army_image.pack()
        self.lbl_current_army_value.pack()

        self.unit_frame = tk.Frame(self)
        for c in army.character_list:
            c_frame = CharacterMenuItem(self.unit_frame, c.name)
            c_frame.pack()
            self.c_frames.append(c_frame)

        self.btn_frame = tk.Frame(self)
        # Buttons
        self.turn_btn = tk.Button(self.btn_frame, text="Turn Start", command=lambda : self.start_turn(parent))
        self.turn_btn.pack()
        self.rmv_btn = tk.Button(self.btn_frame, text="Resolve Battle", command=lambda : self.resolve_battle())
        self.rmv_btn.pack()

        # self.split_button = tk.Button(self.army_frame, text='Split', command=lambda : self.split_army(army))
        # self.split_button.pack(side=tk.LEFT)

        self.army_frame.pack()
        self.unit_frame.pack()
        self.btn_frame.pack()
    
    def start_turn(self, parent):
        if True:
            self.turn_btn.pack_forget()
            self.muster_button = tk.Button(self.army_frame, text='Muster', command=lambda: self.muster_units())
            self.muster_button.pack(side=tk.LEFT)

    def resolve_battle(self):
        ResolveBattleMenu(self)

    def muster_units(self):
        PlayerMusterMenu(self, self.army, self.player)



class ResolveBattleMenu(PlayerArmyBaseMenu):
    army = None

    def __init__(self, parent, *args, **kwargs):
        # unpack parent screen stuff
        parent.turn_btn.pack_forget()
        parent.rmv_btn.pack_forget()
        #self.remove_units_frame = tk.Frame(parent)
        #state what's going on
        self.lbl_rmving = ttk.Label(parent.army_frame, text='Tick boxes of Perished Units', foreground="yellow")
        self.lbl_rmving.pack()
        print(parent.c_frames)
        for c_frame in parent.c_frames:
            if c_frame.character == 'Dragon' : next
            c_frame.update()
        # win/loss checkbox
        self.chck_value = tk.StringVar()
        self.chk_box = ttk.Checkbutton(parent.btn_frame, variable=self.chck_value, text="Win? Leave Unticked if lost")
        self.chk_box.pack()
        # save button
        self.save_button = tk.Button(parent.btn_frame, text="Save", command=lambda : self.save_resolution(parent))
        self.save_button.pack()


    def save_resolution(self, parent):
        # first get rid of stuff
        self.save_button.pack_forget()
        self.chk_box.pack_forget()
        self.lbl_rmving.pack_forget()

        removal_index = []
        # update state and forget
        for i, c_frame in enumerate(parent.c_frames):
            if c_frame.chk_value.get():
                print(f"THIS GUY IS DEAD: {c_frame.character}")
                parent.army.remove_unit(c_frame.character)
                if not parent.army.get_num_units():
                    parent.player.del_army(parent.army.name)
                    print("ALL DEAD")
                removal_index.append(i)
            parent.parent.army_num.set(100)
            c_frame.chk_box.pack_forget()
        parent.c_frames = [c_f for c_f in parent.c_frames if not c_frame.chk_value.get()]
 



# in-depth information about the players armies
class PlayerMusterMenu(PlayerArmyBaseMenu):
    image = ''
    army = None
    c_frames = []

    def __init__(self, parent, army, player, *args, **kwargs):
        self.image = tk.PhotoImage(file=army.symbol)
        # super().__init__(self, parent, army, player, *args, **kwargs)
        # Buttons
        # self.muster_button = tk.Button(self.army_frame, text='Muster', command=lambda: self.muster_unit(army,player, parent))
        # self.muster_button.pack(side=tk.LEFT)
        # self.army_frame.pack(side=tk.LEFT)
        self.muster_frame = tk.Frame(parent)
        # self.split_button.pack_forget()
        parent.muster_button.pack_forget()
        parent.rmv_btn.pack_forget()
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



    def muster_unit(self, army, player, parent):
        pass

    # TODO doesnt update unit list until refresh
    # save selected unit to army
    def save_muster_unit(self, army, player, parent):
        # update objects
        if self.new_unit_select.get(): army.add_character(self.new_unit_select.get())
        player.update_army(army)
        # update interface
        c = CharacterMenuItem(parent.unit_frame, self.new_unit_select.get()).pack()
        parent.lbl_current_army_value['text'] = army.get_value()
        self.c_frames.append(c)
        # return UI to original state
        self.muster_frame.destroy()
        # self.split_button.pack()
        # self.muster_button.pack()
        parent.rmv_btn.pack()
        parent.parent.army_num.set(100) # this triggers update on army overview, unelegant but it works whoot

    def split_army(self):
        pass


    
# to display information about characters in an army
class CharacterMenuItem(tk.Frame):
    character = None
    def __init__(self, parent, character, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.character = character
        self.parent = parent
        self.character_frame = tk.Frame(self.parent)

        self.lbl_character = ttk.Label(self.character_frame, text=character)
        self.chk_value = tk.StringVar()
        self.chk_box = ttk.Checkbutton(self.character_frame, variable=self.chk_value)
        self.lbl_character.pack(side=tk.LEFT)
        self.character_frame.pack()

    def update(self):
        self.chk_box.pack(side=tk.LEFT)

if __name__ == '__main__':
    root = tk.Tk()
    MainClient(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

