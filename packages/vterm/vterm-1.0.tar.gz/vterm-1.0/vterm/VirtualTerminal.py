import tkinter as tk
import threading

RED = "#ff0000"
GREEN = "#00ff00"
BLUE = "#0000ff"
BLACK = "#000000"
WHITE = "#ffffff"
DARKBG = "#2b2b2b"
LIGHTBG = "#3c3f41"
TEXTCOLOR = "#b5b5b5"

class VirtualTerminal(object):
    def __init__(self, startfunction=None, enterfunction=None):
        self.terminal_bgColor = DARKBG
        self.terminal_textColor = TEXTCOLOR
        self.terminal_insertColor = TEXTCOLOR

        self.input_bgColor = DARKBG
        self.input_textColor = TEXTCOLOR
        self.input_insertColor = TEXTCOLOR

        self.divider_height = 1
        self.divider_color = LIGHTBG

        self.terminal_font = ("Menlo-Regular.ttf", 19)
        self.input_font = ("Menlo-Regular.ttf", 19)
        self.title = "VTerminal"
        self.size = (700, 410)

        self.resizable = (True, True)

        self.root = tk.Tk()
        self.position = (int((self.root.winfo_screenwidth() / 2) - (self.size[0] / 2)), int((self.root.winfo_screenheight() / 2) - (self.size[1] / 2)))



        self.root.geometry(f"{self.size[0]}x{self.size[1]}+{self.position[0]}+{self.position[1]}")



        self.root.title(self.title)

        self.root.resizable(self.resizable[0], self.resizable[1])


        self.mainFrame = tk.Frame(self.root, bg=DARKBG)
        self.mainFrame.pack(expand=1, fill="both")

        self.terminalFrame = tk.Frame(self.mainFrame, bg=DARKBG)
        self.terminalFrame.pack(expand=1, fill="both")

        self.terminalDisplay = tk.Text(self.terminalFrame, bg=self.terminal_bgColor, insertbackground=self.terminal_insertColor, fg=self.terminal_textColor, height=1, highlightthickness=0,
                                       borderwidth=2,
                                       relief="flat", font=self.terminal_font)
        self.terminalDisplay.pack(expand=1, fill="both")

        self.terminalDisplay.bind("<Key>", lambda test: "break")

        self.divider = tk.Frame(self.mainFrame, bg=self.divider_color, height=1)
        self.divider.pack(fill="x")

        self.inputFrame = tk.Frame(self.mainFrame, bg=DARKBG, height=40)
        self.inputFrame.pack(fill="x", side="bottom")

        self.inputEntry = tk.Entry(self.inputFrame, bg=self.input_bgColor, relief="flat", fg=self.input_textColor, borderwidth=2, insertbackground=self.input_insertColor, highlightthickness=0, font=self.input_font)
        self.inputEntry.pack(expand=1, fill="both")

        # Can't do right now (on mac)
        # inputButton = tk.Button(inputFrame, text="Enter", relief="flat")
        # inputButton.pack(side="right")

        self.start_function = startfunction
        self.enter_function = enterfunction

        self.inputEntry.bind("<Return>", self.enter_pressed)

        self.asking = False
        self.answer = None



    def update_config(self):
        self.terminalDisplay.config(bg=self.terminal_bgColor,
                                    fg=self.terminal_textColor,
                                    insertbackground=self.terminal_insertColor,
                                    font=self.terminal_font)

        self.inputEntry.config(bg=self.input_bgColor,
                               fg=self.input_insertColor,
                               insertbackground=self.input_insertColor,
                               font=self.input_font)

        self.root.title(self.title)
        self.root.geometry(f"{self.size[0]}x{self.size[1]}+{self.position[0]}+{self.position[1]}")
        self.root.resizable(self.resizable[0], self.resizable[1])
        self.divider.config(height=self.divider_height, bg=self.divider_color)




    def enter_pressed(self, event):
        text = self.inputEntry.get()
        if self.asking:
            self.answer = text
            self.asking = False
        self.inputEntry.delete(0, "end")
        if self.enter_function:
            self.enter_function(text)

    def bind_input(self, function):
        self.enter_function = function
        # self.inputEntry.bind("<Return>", lambda e: function(self.inputEntry.get()))

    def bind_start(self, function):
        self.start_function = function


    def get_terminal(self):
        text = self.terminalDisplay.get(1.0, "end")
        return text[:len(text) - 1]

    def set_terminal(self, text):
        self.terminalDisplay.delete(1.0, "end")
        self.terminalDisplay.insert(1.0, text)

    def rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb


    def config_terminal(self, bgcolor=None, textcolor=None, fontpath=None, fontsize=None):
        if bgcolor:
            if isinstance(bgcolor, tuple):
                self.terminal_bgColor = self.rgb2hex(bgcolor)
            else:
                self.terminal_bgColor = bgcolor


        if textcolor:
            if isinstance(textcolor, tuple):
                self.terminal_textColor = self.rgb2hex(textcolor)
            else:
                self.terminal_textColor = textcolor

        if fontpath:
            self.terminal_font = (fontpath, self.terminal_font[1])

        if fontsize:
            self.terminal_font = (self.terminal_font[0], fontsize)

        self.update_config()

    def config_input(self, bgcolor=None, textcolor=None, fontpath=None, fontsize=None):
        if bgcolor:
            if isinstance(bgcolor, tuple):
                self.input_bgColor = self.rgb2hex(bgcolor)
            else:
                self.input_bgColor = bgcolor

        if textcolor:
            if isinstance(textcolor, tuple):
                self.input_textColor = self.rgb2hex(textcolor)
            else:
                self.input_textColor = textcolor

        if fontpath:
            self.input_font = (fontpath, self.input_font[1])

        if fontsize:
            self.input_font = (self.input_font[0], fontsize)

        self.update_config()

    def config_window(self, title=None, size=None, position=None, resizable=None, dividercolor=None, dividerheight=None):
        if title:
            self.title = title
        if size:
            self.size = size

        if position:
            self.position = position

        if resizable:
            self.resizable = resizable

        if dividercolor:
            if isinstance(dividercolor, tuple):
                self.divider_color = self.rgb2hex(dividercolor)
            else:
                self.divider_color = dividercolor

        if dividerheight:
            self.divider_height = dividerheight

        self.update_config()

    def print(self, text, end="\n"):
        self.set_terminal(self.get_terminal() + text + end)


    def input(self):
        self.asking = True

        while not self.answer:
            pass
        self.answer = None

        return self.answer



    def cancel_input(self):
        self.asking = False


    def mainloop(self):
        if self.start_function:
            threading.Thread(target=self.start_function).start()
        self.root.mainloop()