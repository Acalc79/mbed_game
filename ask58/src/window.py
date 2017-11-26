import tkinter as tk
from tkinter import Tk, Frame, Grid, Button, Text
from game import Game
import server

STICK_ALL = tk.N+tk.S+tk.W+tk.E

WIDTH = 360
HEIGHT = 240
BTN_PAD_X = 10
BTN_PAD_Y = 10

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.difficulty = 1
        self.grid(row=0, column=0, sticky=STICK_ALL)
        Grid.rowconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        self.master.minsize(width=WIDTH, height=HEIGHT)
        self.master.title("Mbed space game")
        self.row_now = 0
        self.create_menu_message()
        self.create_buttons()

    def place_item(self, item):
        item.grid(row=self.row_now, column=0,
                  padx=BTN_PAD_X, pady=BTN_PAD_Y,
                  sticky=STICK_ALL)
        Grid.rowconfigure(self, self.row_now, weight=1)
        self.row_now += 1
        
    def create_menu_message(self):
        self.menu_msg = Text(self, height=2, width=30)
        self.menu_msg.insert(tk.END, "WELCOME!\nThe cloud invaders await you")
        self.place_item(self.menu_msg)

    def create_buttons(self):
        self.play_btn = Button(self, text="PLAY", command=self.play_game)
        self.place_item(self.play_btn)
        
        self.settings_btn = Button(self, text="DIFFICULTY: "+str(self.difficulty),
                                   command=self.toggle_difficulty)
        self.place_item(self.settings_btn)
        
        self.quit_btn = Button(self, text="QUIT",
                               command=root.destroy)
        self.place_item(self.quit_btn)

    def toggle_difficulty(self):
        self.difficulty = self.difficulty % 3 + 1
        self.settings_btn['text'] = "DIFFICULTY: "+str(self.difficulty)
        
    def play_game(self):
        httpd = server.run()
        game = Game(httpd.handle_request, self.difficulty)
        server.set_game(game)
        game.start_game()

root = Tk()
app = Application(master=root)
app.mainloop()
