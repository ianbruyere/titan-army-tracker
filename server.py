import tkinter as tk
import socket
import threading
from time import sleep

class Server():
    server = None
    HOST_ADDR = "0.0.0.0"
    HOST_PORT = 8080
    client_name = " "
    clients = []
    clients_names = []
    game_started = False

    def __init__(self, *arg, **args):
        self.window = tk.Tk()
        self.window.title("Titan Army Tracker Server")
    
        # Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
        self.topFrame = tk.Frame(self.window)
        self.btnStart = tk.Button(self.topFrame, text="Connect", command=lambda : self.start_server())
        self.btnStart.pack(side=tk.LEFT)
        self.btnStop = tk.Button(self.topFrame, text="Stop", command=lambda : self.stop_server(), state=tk.DISABLED)
        self.btnStop.pack(side=tk.LEFT)
        self.topFrame.pack(side=tk.TOP, pady=(5, 0))
    
        # Middle frame consisting of two labels for displaying the host and port info
        self.middleFrame = tk.Frame(self.window)
        self.lblHost = tk.Label(self.middleFrame, text = "Host: X.X.X.X")
        self.lblHost.pack(side=tk.LEFT)
        self.lblPort = tk.Label(self.middleFrame, text = "Port:XXXX")
        self.lblPort.pack(side=tk.LEFT)
        self.middleFrame.pack(side=tk.TOP, pady=(5, 0))
        # The client frame shows the client area
        self.clientFrame = tk.Frame(self.window)
        self.lblLine = tk.Label(self.clientFrame, text="*******************CLIENT LIST*****************").pack()
        self.scrollBar = tk.Scrollbar(self.clientFrame)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tkDisplay = tk.Text(self.clientFrame, height=15, width=40)
        self.tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.scrollBar.config(command=self.tkDisplay.yview)
        self.tkDisplay.config(yscrollcommand=self.scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
        self.clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

        self.window.mainloop()

    # start server function
    def start_server(self):
    
        self.btnStart.config(state=tk.DISABLED)
        self.btnStop.config(state=tk.NORMAL)

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.HOST_ADDR, self.HOST_PORT))
        server.listen(5)

        threading._start_new_thread(self.accept_clients, (server, " "))

        self.lblHost["text"] = f"Host: {self.HOST_ADDR}"
        self.lblPort["text"] = f"Port: {self.HOST_PORT}"

    def stop_server(self):
        self.btnStart.config(state=tk.NORMAL)
        self.btnStop.config(state=tk.DISABLED)

    def accept_clients(self, the_server, y):
        while True:
            if len(self.clients) < 2:
                client, addr = the_server.accept()
                self.clients.append(client)

                # use a thread so as not to clog the gui thread
                threading._start_new_thread(self.send_recieve_client_message, (client, addr))

    def send_recieve_client_message(self, client_connection, client_ip_addr):
        client_msg = " "

        # send welcome message to client
        client_name = client_connection.recv(4096)
        client_connection.send(f"Welcome {client_name}. Use 'exit' to quit")

        self.clients_names.append(client_name)

        self.update_client_names_display(self.clients_names) # updatre client names display

        while True:
            data = client_connection.recv(4096)
            if not data: break
            if data == "exit": break

            client_msg = data

            idx = self.get_client_index(self.clients, client_connection)
            sending_client_name = self.clients_names[idx]

            for c in self.clients:
                if c != client_connection:
                    c.send(f"{sending_client_name} => {client_msg}")

        # find the client index then remove from both lists(client name list and connection list)
        idx = self.get_client_index(self.clients, client_connection)
        del self.clients_names[idx]
        del self.clients[idx]
        client_connection.close()

        self.update_client_names_display(self.clients_names) # update client names display

    # Helper function to return index of current client in list of clients
    def get_client_index(client_list, curr_client):
        idx = 0
        for conn in client_list:
            if conn == curr_client:
                break
            idx += 1

        return idx

# Update client name to display when client connects or disconnect
    def update_client_names_display(self, name_list):
        self.tkDisplay.config(state=tk.NORMAL)
        self.tkDisplay.config('1.0', tk.END)

        for c in name_list:
            self.tkDisplay.insert(tk.END, c+"\n")
        self.tkDisplay.config(state=tk.DISABLED)

if __name__ == '__main__':
    app = Server()
    app()
