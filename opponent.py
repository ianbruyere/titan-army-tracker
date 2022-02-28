import tkinter as tk
import tkinter.ttk as ttk


BIG_FONT = ("Times New Roman", 24)
FONT = ("Times New Roman", 16)

class OpponentFrame(tk.Frame):

    def __init__(self, parent, opponent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.opponent_frame = tk.Frame(self.parent, highlightbackground=opponent.color, highlightthickness=4)

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

        self.armies_frame.pack(side=tk.BOTTOM, pady=(10, 10))
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