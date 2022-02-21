import socket
import threading
import os
import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from turtle import width


class ClientSetupScreen():

    OPTIONS = [
    "Black",
    "Yellow",
    ] #etc
    images = {}
    HOST_ADDR = "0.0.0.0"
    HOST_PORT = 8080
    your_name = ''
    client = ''

    def __init__(self, *args, **kwargs):
        # Setup Window
        self.root = tk.Tk()
        self.root.title("Titan Tracker Client")

        self.top_welcome_frame = tk.Frame(self.root)
        self.lbl_name = ttk.Label(self.top_welcome_frame, text = "Name:")
        self.lbl_name.pack(side=tk.LEFT)
        self.ent_name = tk.Entry(self.top_welcome_frame)
        self.ent_name.pack(side=tk.LEFT)
        self.btn_connect = tk.Button(self.top_welcome_frame, text="Connect", command=lambda : self.connect())
        self.btn_connect.pack(side=tk.LEFT)
        self.top_welcome_frame.pack(side=tk.TOP)

        # Middle frame consisting of Team Selection
        self.middleFrame = tk.Frame(self.root, width=100, height=100)
        self.optionTeam = tk.StringVar(self.middleFrame)
        self.optionTeam.set('--- Select ---')
        self.lblTeam = tk.OptionMenu(self.middleFrame, self.optionTeam , *self.OPTIONS)
        self.optionTeam.trace("w", self.load_armies)
        self.lblTeam.pack(side=tk.LEFT)
        self.middleFrame.pack(side=tk.TOP, pady=(5, 0))
        # army one setup
        self.army_one_frame = tk.Frame(self.root, width=100, height=100)
        self.army_select_one = tk.StringVar(self.army_one_frame)
        self.army_select_one.trace("w", self.change_army_one)
        self.lbl_army_one = ttk.Label(self.army_one_frame, text='Army 1 Select')
        self.lbl_army_one.pack()
        self.army_one_frame.pack(side=tk.TOP, pady=(5, 0))
        # army two setup
        self.army_two_frame = tk.Frame(self.root, width=100, height=100)
        self.army_select_two = tk.StringVar(self.army_two_frame)
        self.army_select_two.trace("w", self.change_army_two)
        self.lbl_army_two = ttk.Label(self.army_two_frame, text='Army 2 Select')
        self.lbl_army_two.pack()
        self.army_two_frame.pack(side=tk.TOP, pady=(5, 0))

        self.root.mainloop()

    def change_army_one(self, *args):
        self.lbl_army_one['image'] = self.images[self.army_select_one.get()]

    def change_army_two(self, *args):
        self.lbl_army_two['image'] = self.images[self.army_select_two.get()]

    def load_armies(self, *args):
        path = f"./game_data/{self.optionTeam.get()}/"
        file_names = os.listdir(path)
        file_paths = [path + file_name for file_name in file_names]
        print(file_paths)
        self.images = dict(zip(file_names, [tk.PhotoImage(file=file_path) for file_path in file_paths]))
        print(self.images)
        # setting up first army select
        self.dd_army_one = tk.OptionMenu(self.army_one_frame, self.army_select_one, *file_names)
        self.dd_army_one.pack(side=tk.LEFT)
        # setting image for first army selected
        self.lbl_army_one['image'] = list(self.images.values())[0]

        #  setting up second army select
        self.dropdown_army_two = tk.OptionMenu(self.army_two_frame, self.army_select_two, *file_names)

        self.dropdown_army_two.pack(side=tk.LEFT)
        # setting image for first army selected
        self.lbl_army_two['image'] = list(self.images.values())[1]

    def connect_to_server(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.HOST_ADDR, self.HOST_PORT))
            self.client.send(self.your_name) # send name to server after connecting

            # disable widgets
            self.btn_connect.config(state=DISABLED)
            self.ent_name.config(state=DISABLED)
            self.bl_name.config(state=DISABLED)
            enable_disable_buttons("disable")

            # start a thread to keep recieving message from server
            # do not block main thread
            threading._start_new_thread(self.recieve_message_from_server, ("m"))
        except Exception as e:
            tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + self.HOST_ADDR + 
            " on port: " + str(self.HOST_PORT) + " Server may be Unavailable. Try again later")


    def connect(self):
        if len(self.ent_name.get()) < 1:
            tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name")
        else:
            your_name = self.ent_name.get()
            self.lbl_name["text"] = "Your name: " + your_name
            self.connect_to_server()

    def recieve_message_from_server(self, m):
        while True:
            from_server = self.client.recv(4096)

            if not from_server: break

            if from_server.startswith("welcome"):
                if from_server == "welcome1":
                    self.lbl_welcome["text"] = f"Server says: Welcome {self.your_name}! Waiting for other players"
                self.lbl_line_server.pack()

        self.client.close()
        self.window.destroy()

    def send_message_to_server(self, msg):
        self.client.send(msg)
        if msg == "exit":
            self.client.close()
            self.window.destroy()
    


if __name__ == '__main__':
    app = ClientSetupScreen()