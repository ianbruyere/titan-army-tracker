from faulthandler import disable
from re import L
from typing import overload
from player import *
from opponent import *
from game_data.character_data import Characters
import socket
import threading
import os
import math
import tkinter as tk
import tkinter.ttk as ttk

BIG_FONT = ("Times New Roman", 24)
FONT = ("Times New Roman", 16)

######## TESTING DATA ############
test_character_one = Characters["Dragon"]
test_character_seven = Characters["Dragon"]
test_character_two = Characters["Serpent"]
test_character_three = Characters["Titan"]
test_character_four = Characters["Angel"]

list_characters_one = [test_character_one]
list_characters_seven = [test_character_seven]
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
test_player.add_army("g_fish", list_characters_seven)
test_player.add_army("g_snake", list_characters_four)
test_player.add_score(747)

test_opponents = {"John" : test_opponent_one, "Cash": test_opponent_two}
############## END TESTING DATA ######################


class PlayerClient(tk.Frame):
    opponents =  test_opponents # opponent name : opponent data
    my_turn = True # TODO for DEBUGGING ONLY
    turn_number = -1
    army_frames = {}
    opponent_frames = []

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.title("Titan Main Client")
        self.player = test_player

        self.init_player()
        self.make_opponents()

    # will create an opponent object with provided info and tie it into the board
    def make_opponents(self):
        self.opponent_frame = tk.Frame(self.root)
        self.opponent_update_trigger = tk.StringVar()
        self.opponent_update_trigger.trace('w', self.update_opponents)
        for opponent in self.opponents.values():
            opponent_frame = OpponentFrame(self.opponent_frame, opponent)
            opponent_frame.pack()
        self.opponent_frame.pack()

    # will make the player object to keep track of main users
    # army info and allow managing of armies wehn turn
    def init_player(self):
        self.player_frame = tk.Frame(self.root, highlightbackground=self.player.color, highlightthickness=4)
        
        self.player_scoreboard = tk.Frame(self.player_frame)
        self.lbl_name = ttk.Label(self.player_scoreboard, text = self.player.name, font=BIG_FONT)
        self.lbl_score = ttk.Label(self.player_scoreboard, text = self.player.score, font=BIG_FONT, foreground="green")
        self.lbl_name.pack(side=tk.LEFT)
        self.lbl_score.pack(side=tk.LEFT)
        self.player_scoreboard.pack(side=tk.LEFT)


        self.army_frame = tk.Frame(self.player_frame)
        for army in self.player.get_armies().values():
            new_frame = PlayerArmyOverview(self, army)
            self.army_frames[army.name] = new_frame
            new_frame.pack()
            
        self.army_overview_trigger = tk.StringVar()
        self.army_overview_trigger.trace('w', self.update_army_overview)
        self.army_frame.pack(side=tk.LEFT)
        self.player_frame.pack()
        
    def update_opponents(self, *args):
        self.opponent_frame.destroy()
        self.make_opponents()

    def update_army_overview(self, *args):
        # destroying
        removal = []
        # get rid of army display if it has no units
        for a_frame in self.army_frames.values():
            if not a_frame.army.get_num_units():
                removal.append(a_frame.army.name)
                a_frame.destroy_myself()
        # remove from the army frames
        self.army_frames = {k:v for k,v in self.army_frames.items() if k not in removal}
        # create new army frames in result of army creation
        for army in self.player.get_armies().values():
            if army.name not in self.army_frames.keys():
                new_frame = PlayerArmyOverview(self, army)
                self.army_frames[army.name] = new_frame
                new_frame.pack()


# contains information about player armies, score
class PlayerArmyOverview(tk.Frame):

    def __init__(self, parent, army, *args, **kwargs):
        tk.Frame.__init__(self, parent.army_frame, *args, **kwargs)
        self.image = tk.PhotoImage(file=army.symbol)
        self.army = army
        self.client = parent

        self.army_value_trigger = tk.StringVar()
        self.army_value_trigger.set(str(army.get_value()))
        self.army_value_trigger.trace("w", self.update_lbls)
        self.army_num_trigger = tk.StringVar()
        self.army_num_trigger.set(str(army.get_num_units()))
        self.army_num_trigger.trace("w", self.update_lbls)
        
        self.army_frame = tk.Frame(self)
        self.lbl_army = ttk.Label(self.army_frame, image=self.image)
        self.lbl_army.bind("<Button-1>", lambda e : self.open_menu(e))
        self.lbl_units = ttk.Label(self.army_frame, text=self.army_num_trigger.get(), font=BIG_FONT)
        self.lbl_value = ttk.Label(self.army_frame, text=self.army_value_trigger.get(), font=BIG_FONT, foreground = "cyan")


        self.lbl_army.pack()
        self.lbl_units.pack(side=tk.LEFT)
        self.lbl_value.pack(side=tk.RIGHT)
        self.army_frame.pack()
        self.pack(side=tk.LEFT)

    def open_menu(self, event):
        PlayerArmyBaseMenu(self, self.army)

    def update_lbls(self, *args):
        self.lbl_units['text'] = self.army.get_num_units()
        self.lbl_value['text'] = self.army.get_value()

    
    def destroy_myself(self):
        for widget in self.winfo_children():
            print("Destroying Myself")
            widget.destroy()
        self.destroy()

    def update_frame(self, parent, army):
        for widget in self.winfo_children():
            print("Updating Myself")
            widget.destroy()
        self.__init__(parent, army)



class PlayerArmyBaseMenu(tk.Toplevel):
    btn_frames = []

    def __init__(self, parent, army, *args, **kwargs):
        tk.Toplevel.__init__(self)
        self.c_frames = []
        self.image = tk.PhotoImage(file=army.symbol)
        self.army = army
        self.title(army.name)
        self.army_overview = parent

        # army info
        self.army_frame = tk.Frame(self)
        self.lbl_current_army = ttk.Label(self.army_frame, text = "Current Army")
        self.lbl_current_army_image = ttk.Label(self.army_frame, image=self.image, text = "WHY NO SHOW UP")
        self.lbl_current_army_value = ttk.Label(self.army_frame, text = str(army.get_value()), foreground="cyan")
        # pack army info
        self.lbl_current_army.pack()
        self.lbl_current_army_image.pack()
        self.lbl_current_army_value.pack()
        self.army_frame.pack()
        # unit frame
        self.unit_frame = tk.Frame(self)
        self.update_unit_frame_trigger = tk.StringVar(self.unit_frame)
        self.update_unit_frame_trigger.trace('w', self.update_unit_frame)

        for c in self.army.character_list:
            c_frame = CharacterMenuItem(self.unit_frame, c.name)
            c_frame.pack()
            self.c_frames.append(c_frame)

        self.unit_frame.pack()
        # Buttons
        self.btn_frame = tk.Frame(self)
        # self.turn_btn = tk.Button(self.btn_frame, text="Turn Start", command=lambda : self.start_turn())
        # self.turn_btn.pack()
        self.split_btn = tk.Button(self.btn_frame, text='Split?', command=lambda : self.split_army())
        self.split_btn.pack(side=tk.LEFT)
        self.resolve_btn = tk.Button(self.btn_frame, text="Resolve Battle", command=lambda : self.resolve_battle())
        self.muster_button = tk.Button(self.btn_frame, text='Muster', command=lambda: self.muster_units())
        self.muster_button.pack(side=tk.LEFT)
        self.resolve_btn.pack(side=tk.LEFT)
        self.btn_frame.pack()
    



    def resolve_battle(self):
        ResolveBattleMenu(self)

    def muster_units(self):
        PlayerMusterMenu(self)
    
    def split_army(self):
        SplitArmyMenu(self)

    def update_unit_frame(self, *args):
        # destroy
        self.unit_frame.destroy()
        self.c_frames = []
        if not len(self.army.character_list):
            self.destroy()
            return
        # rebuild
        self.unit_frame = tk.Frame(self)
        # populate
        for c in self.army.character_list:
            c_frame = CharacterMenuItem(self.unit_frame, c.name)
            c_frame.pack()
            self.c_frames.append(c_frame)
        # present
        self.unit_frame.pack()



class SplitArmyMenu(PlayerArmyBaseMenu):
    def __init__(self, parent, *args, **kwargs):
        self.base_menu = parent
        # unpack parent screen stuff
        self.base_menu.btn_frame.pack_forget()

        # help message
        self.lbl_splitting = ttk.Label(self.base_menu.army_frame, text='Tick Units To Move', foreground="yellow")
        self.lbl_splitting.pack()
        # unhide chk_box
        for c_frame in self.base_menu.c_frames:
            c_frame.unhide_chk_box()

        # army selection setup
        player = self.base_menu.army_overview.client.player
        path = f"./game_data/{player.color}/"
        file_names = [file_name for file_name in os.listdir(path) if file_name not in player.armies.keys()]
        file_paths = [path + file_name for file_name in file_names if file_name not in player.armies.keys()]
        file_names = [file_name.split(".")[0] for file_name in file_names]
        self.images = dict(zip(file_names, [tk.PhotoImage(file=file_path) for file_path in file_paths]))
        # setup to hold dd value and trigger image change
        self.army_selected = tk.StringVar()
        self.army_selected.trace('w', self.update_image_new_army)
        # frame for new army
        self.new_army_frame = tk.Frame(self.base_menu)
        self.lbl_new_army = ttk.Label(self.new_army_frame, text='New Army Select')
        self.lbl_new_army.pack()
        self.lbl_new_army['image'] = list(self.images.values())[0]
        self.dd_army = tk.OptionMenu(self.new_army_frame, self.army_selected, *file_names)
        self.dd_army.pack()
        # save button
        self.btn_save = tk.Button(self.new_army_frame, text='Save', command= lambda: self.save(player))
        self.btn_save.pack()
        self.new_army_frame.pack(side=tk.LEFT)

    def update_image_new_army(self, *args):
        self.lbl_new_army['image'] = self.images[self.army_selected.get()]

    def save(self, player):
        # get units moving
        new_units = [Characters[c_frame.character] for c_frame in self.base_menu.c_frames if c_frame.chk_value.get()]
        # create new army with units
        player.add_army(self.army_selected.get(), new_units)
        # remove units from old army
        for unit in new_units:
            self.base_menu.army.remove_unit(unit)
        # set screen back to base menu state
        self.btn_save.pack_forget()
        self.lbl_splitting.pack_forget()
        self.new_army_frame.destroy()
        # update screens accordingly
        self.base_menu.update_unit_frame_trigger.set(200)
        self.base_menu.army_overview.client.army_overview_trigger.set(300)
        self.base_menu.army_overview.army_num_trigger.set(100)


class ResolveBattleMenu(PlayerArmyBaseMenu):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self)
        self.base_menu = parent
        # unpack parent screen stuff
        # self.base_menu.turn_btn.pack_forget()
        self.base_menu.btn_frame.pack_forget()
        # state what's going on
        self.lbl_rmving = ttk.Label(self.base_menu.army_frame, text='Tick Perished Units', foreground="yellow")
        self.lbl_rmving.pack()

        for c_frame in self.base_menu.c_frames:
            c_frame.unhide_chk_box()

        # win/loss checkbox
        self.win_loss_frame = tk.Frame(self.base_menu)
        self.chk_loss_value = tk.StringVar()
        self.chk_loss_box = ttk.Checkbutton(self.win_loss_frame, variable=self.chk_loss_value, text="Lose?")
        self.chk_loss_box.pack()
        # surrender
        self.surrender = tk.StringVar()
        self.chk_surrender = ttk.Checkbutton(self.win_loss_frame, variable=self.surrender, text="Surrendered?")
        self.chk_surrender.pack()

        # loss to?
        self.victor = tk.StringVar()
        self.lbl_opponents = ttk.Label(self.win_loss_frame, text="Who did you lose to?")
        self.lbl_opponents.pack(side=tk.LEFT)
        self.dd_opponents = tk.OptionMenu(self.win_loss_frame, self.victor, *list(self.base_menu.army_overview.client.opponents.keys()))
        self.dd_opponents.pack(side=tk.LEFT)

        self.win_loss_frame.pack()
        # save button
        self.btn_frame = tk.Frame(self)
        self.save_button = tk.Button(self.base_menu, text="Save", command=lambda : self.save_resolution())
        self.save_button.pack()
        self.btn_frame.pack()

    def save_resolution(self):
        # first get rid of stuff
        self.save_button.pack_forget()
        # self.chk_box.pack_forget()
        self.lbl_rmving.pack_forget()
        self.btn_frame.pack_forget()
        self.win_loss_frame.pack_forget()
        removal_index = []

        
        # if person lost, get points now
        if self.chk_loss_value.get():
            opponent = self.base_menu.army_overview.client.opponents[self.victor.get()]
            total_points = self.base_menu.army.get_value()
            if self.surrender.get():
                total_points = math.floor(total_points / 2)
            opponent.add_score(total_points)

        # update state and forget
        for i, c_frame in enumerate(self.base_menu.c_frames):
            if c_frame.chk_value.get():
                self.base_menu.army.remove_unit(c_frame.character)
                # remove army if 0 units
                if not self.base_menu.army.get_num_units():
                    self.base_menu.army_overview.client.player.del_army(self.base_menu.army.name)
                removal_index.append(i)
            c_frame.chk_box.pack_forget()
            
        # update UI
        self.base_menu.c_frames = [c_f for c_f in self.base_menu.c_frames if not c_frame.chk_value.get()]
        self.base_menu.update_unit_frame_trigger.set(100)
        self.base_menu.army_overview.client.army_overview_trigger.set(300)
        self.base_menu.army_overview.army_num_trigger.set(200)
        self.base_menu.army_overview.client.opponent_update_trigger.set(266)
        
 



# in-depth information about the players armies
class PlayerMusterMenu(PlayerArmyBaseMenu):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self)
        self.base_menu = parent
        # take care of stuff on base menu
        self.base_menu.muster_button.pack_forget()
        self.base_menu.resolve_btn.pack_forget()
        # makes the stuff
        self.muster_frame = tk.Frame(self.base_menu)
        self.lbl_mustering = ttk.Label(self.muster_frame, text="You are Mustering", foreground='yellow', font=FONT)
        self.new_unit_select = tk.StringVar(self.muster_frame)
        self.characters = tk.OptionMenu(self.muster_frame, self.new_unit_select, *[c for c in Characters.keys()])
        self.save_button = tk.Button(self.muster_frame, text="Save", command=lambda : self.save_muster_unit())
        # sub units pack
        self.lbl_mustering.pack()
        self.characters.pack()
        self.save_button.pack()
        # main local frame
        self.muster_frame.pack(side=tk.LEFT)

    # save selected unit to army
    def save_muster_unit(self):
        # update objects
        if self.new_unit_select.get(): self.base_menu.army.add_character(self.new_unit_select.get())
        self.base_menu.army_overview.client.player.update_army(self.base_menu.army)
        # update interface
        c = CharacterMenuItem(self.base_menu.unit_frame, self.new_unit_select.get())
        c.pack()
        self.base_menu.lbl_current_army_value['text'] = self.base_menu.army.get_value()
        self.base_menu.c_frames.append(c)
        # return UI to original state
        self.muster_frame.destroy()
        self.base_menu.resolve_btn.pack()
        # update overview screen
        self.base_menu.army_overview.army_value_trigger.set(100)


    
# to display information about characters in an army
class CharacterMenuItem(tk.Frame):

    def __init__(self, parent, character, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.character = character
        self.base_menu = parent
        self.character_frame = tk.Frame(self.base_menu)

        self.lbl_character = ttk.Label(self.character_frame, text=character)
        self.chk_value = tk.StringVar()
        self.chk_box = ttk.Checkbutton(self.character_frame, variable=self.chk_value)
        self.lbl_character.pack(side=tk.LEFT)
        self.character_frame.pack()

    def unhide_chk_box(self):
        self.chk_box.pack(side=tk.LEFT)

if __name__ == '__main__':
    root = tk.Tk()
    PlayerClient(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

