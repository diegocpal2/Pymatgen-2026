import sys
import tkinter as tk

from alignn_handler import AlignnGuiHandler

command_list = {
    "Download database from The Materials Project.": 1,
    "Prepare database for training.": 2,
    "Train model.": 3,
    "Evaluate model.": 4,
    "Formula lookup.": 5,
    "Predict property after applying strain to the structure.": 6,
    "Predict property after changing structure atoms.": 7,
}

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alignn GUI")
        self.geometry("720x720")

class GUI_functions(tk.Frame):
    def __init__(self, root):

        self.root = root
        self.refresh_app()

    def refresh_app(self):
        self.command_selector()
        self.draw_main_button_frame()
        self.draw_text_box()

    def command_selector(self):
        insert_position = tk.END
        pack_side = tk.LEFT
        list_width = 100
        self.command_selector = tk.Listbox(self.root, width=list_width)
        self.command_selector.pack()
        for command in command_list.keys():
            self.command_selector.insert(insert_position, command)

    def draw_main_button_frame(self):
        self.main_buttons = tk.Frame(self.root, bg='green')
        self.main_buttons.pack()
        self.draw_buttons()

    def draw_buttons(self):
        button_frame = self.main_buttons
        button_align = 'left'
        handler = self.handler
        handler.commands = ["hardcoded"]
        self.run_button = tk.Button(self.root, text="Run Selected", command=lambda:handler.download_db())
        self.run_all_button = tk.Button(self.root, text="Run all")
        self.help_button = tk.Button(self.root, text="Help") #help="Display information about program and help guide")

        self.run_button.pack(in_=button_frame, side=button_align)
        self.run_all_button.pack(in_=button_frame, side=button_align)
        self.help_button.pack(in_=button_frame, side=button_align)

    def draw_text_box(self):
        text_placement = tk.END
        self.text = tk.Text(self.root, 
                            background="black", 
                            foreground="yellow")
        print(self.handler.process)
        if self.handler.process:
            print("estamos LLEGANDO")
            stdout, stderr = self.handler.process.communicate()
            if stdout:
                for line in stdout:
                    self.text.insert(text_placement, line)
            if stderr:
                for line in stderr:
                    self.text.insert(text_placement, line)
        self.text.pack(expand=True)
                    
# ayo fuck oop
gui = GUI()
function = GUI_functions(gui)
function.refresh_app()
handler = AlignnGuiHandler()
gui.mainloop()