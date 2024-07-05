import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

class GameClient:
    def _init_(self, master):
        self.master = master
        self.master.title("Batu, Air, Burung Game")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.player_name = simpledialog.askstring("Name", "Enter your name:", parent=self.master)
        self.send_message(f"NAME:{self.player_name}")

        self.label_name = tk.Label(master, text=f"Player Name: {self.player_name}")
        self.label_name.pack(pady=10)

        self.label_turn = tk.Label(master, text="Waiting for other player to join...")
        self.label_turn.pack(pady=10)

        self.label_score = tk.Label(master, text="Scores: ")
        self.label_score.pack(pady=10)

        self.label_winner = tk.Label(master, text="")
        self.label_winner.pack(pady=10)

        self.batu_button = tk.Button(master, text="Batu", command=lambda: self.send_choice("batu"))
        self.air_button = tk.Button(master, text="Air", command=lambda: self.send_choice("air"))
        self.burung_button = tk.Button(master, text="Burung", command=lambda: self.send_choice("burung"))

        self.setup_buttons()

        threading.Thread(target=self.receive_messages).start()

    def send_message(self, msg):
        self.client.send(msg.encode(FORMAT))

    def receive_message(self):
        return self.client.recv(1024).decode(FORMAT)

    def send_choice(self, choice):
        self.send_message(f"{self.player_name}:{choice}")

    def receive_messages(self):
        while True:
            message = self.receive_message()

            if "Turn:" in message:
                self.label_turn.config(text=message)
                if self.player_name in message:
                    self.enable_buttons()
                else:
                    self.disable_buttons()
            elif "Scores" in message:
                self.label_score.config(text=message)
            elif "wins the game" in message or "The game is a tie" in message:
                self.label_winner.config(text=message)
                messagebox.showinfo("Game Over", message)
                self.client.close()
                self.master.quit()
                break
            else:
                self.label_turn.config(text=message)
        
    def setup_buttons(self):
        self.batu_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.air_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.burung_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.disable_buttons()

    def disable_buttons(self):
        self.batu_button.config(state=tk.DISABLED)
        self.air_button.config(state=tk.DISABLED)
        self.burung_button.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.batu_button.config(state=tk.NORMAL)
        self.air_button.config(state=tk.NORMAL)
        self.burung_button.config(state=tk.NORMAL)

def start_client():
    root = tk.Tk()
    client = GameClient(root)
    root.mainloop()

if __name__ == "_main_":
    start_client()

    