import tkinter as ttk
import tkinter.ttk as ttk
import tkinter.messagebox
import threading
from PIL import Image
import customtkinter
import subprocess
import sys
import os

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        print(f'printing working directory: {os.getcwd()}')

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        self.minsize(900, 600)

        # load logo images
        icon_light = Image.open("icon_light.png")
        icon_dark = Image.open("icon_dark.png")
        icon_bit = Image.open("bit_icon.ico")

        # image access test

        file_path = './icon_light.png'
        if os.path.exists(file_path):
            print('File exists and the script has access to it.')
        else:
            print('File does not exist or the script does not have access to it.')

        # configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # create column 0, row 0 (logo) frame
        self.logo_frame = customtkinter.CTkFrame(self, corner_radius=0, width=140)

        # create column 0, row 1 (button) frame
        self.button_frame = customtkinter.CTkFrame(self, corner_radius=0, width=140)

        # create column 1, row 2 (treeview) frame
        self.treeview_frame = customtkinter.CTkFrame(self, corner_radius=0)

                                        ##### create column 0 widgets #####

        # logo: column 0, row 0
        # title of the program
        self.logo_label = customtkinter.CTkLabel(self.logo_frame, text="LAN Pigeon",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        # import of image and convert to label
        #self.logo_icon = customtkinter.CTkImage(light_image=icon_light,
        #                                        dark_image=icon_dark,
        #                                        size=(150, 115))
        #self.icon_label = customtkinter.CTkLabel(self.logo_frame, image=self.logo_icon, anchor=tkinter.CENTER, text='')

        # buttons: column 0, row 1
        # button 1
        self.button1 = customtkinter.CTkButton(self.button_frame, command=self.button_click, text='Save Results')

        # button 2
        self.button2 = customtkinter.CTkButton(self.button_frame, command=self.button_click, text='Placeholder')

        # button 3
        self.button3 = customtkinter.CTkButton(self.button_frame, text='CMD Version',
                                               command=lambda: threading.Thread(target=self.cmd_version_click).start())

        # button 4
        self.button4 = customtkinter.CTkButton(self.button_frame, command=self.button_click, text='Exit')


                                        ##### create column 1 widgets #####

        # treeview: column 1, row 2
        # Create the results treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#333", foreground="#fff", fieldbackground="#333")
        self.style.map("Treeview", background=[("selected", "#444")])
        self.style.configure('Treeview.Heading', background="#444", foreground="#fff")
        self.label_treeview = customtkinter.CTkLabel(master=self.treeview_frame, width=250, text="Results",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.results_columns = ('IP Address', 'Hostname', 'MAC Address', 'Ping', 'Connectivity')
        self.results_treeview = ttk.Treeview(self.treeview_frame, columns=self.results_columns,
                                             show='headings', height=23)
        # Configure the results treeview columns
        for column in self.results_columns:
            self.results_treeview.heading(column, text=column)
            self.results_treeview.column(column, anchor='center', width=150)
        # Create a scrollbar for the results treeview
        self.results_scrollbar = ttk.Scrollbar(self.treeview_frame, orient='vertical', command=self.results_treeview.yview)
        self.results_treeview.configure(yscrollcommand=self.results_scrollbar.set)

        #self.button5 = customtkinter.CTkButton(self, command=self.button_click)

        # pack column 0, row 0 (logo) frame with widgets
        #self.logo_label.grid(column=0, row=0, padx=(17, 0), sticky='new')
        #self.icon_label.grid(column=0, row=1, padx=(17, 0), sticky='new')

        # pack column 0, row 1 (button) frame with widgets
        self.button1.grid(column=0, row=0, padx=20, pady=(10, 10), sticky='ew')
        self.button2.grid(column=0, row=1, padx=20, pady=(10, 10), sticky='ew')
        self.button3.grid(column=0, row=2, padx=20, pady=(10, 10), sticky='ew')
        self.button4.grid(column=0, row=3, padx=20, pady=(10, 10), sticky='ew')

        # pack column 1 with widgets
        #self.button2.grid(row=0, column=1)
        self.label_treeview.grid(row=1, column=0, columnspan=4, rowspan=1, sticky='new')
        self.results_treeview.grid(row=2, column=0, columnspan=4, sticky="nsew")
        self.results_scrollbar.grid(row=2, column=5, pady=(20, 0), padx=(0, 20), sticky='ns', rowspan=1)

        # frame create
        self.logo_frame.grid(row=0, column=0,rowspan=2, sticky="nwe")
        self.button_frame.grid(row=1, column=0,rowspan=4, sticky="swe")
        self.treeview_frame.grid(row=0, column=1,rowspan=2, sticky="nswe")

        self.mainloop()

    # add methods to app
    def button_click(self):
        print("button click")

    def cmd_version_click(self):
        # set terminal based on OS
        if sys.platform.startswith('win'):
            # For Windows
            cmd = 'start cmd /c python scan_test.py'
        elif sys.platform.startswith('darwin'):
            # For Mac
            cmd = 'open -a Terminal python scan_test.py'
        else:
            # For Linux
            cmd = 'gnome-terminal -x python scan_test.py'

        # Spawn a new process to run the command in a separate terminal window
        subprocess.run(['start', '/b', 'cmd', '/c', 'python', 'scan_test.py'], shell=True)
        #subprocess.run(['x-terminal-emulator', '-e', 'python /path/to/your/script.py'])
        # create sidebar frame with widgets


        # create main entry and button


        # create textbox


        # create tabview


        # create radiobutton frame


        # create slider and progressbar frame


        # create scrollable frame


        # create checkbox and switch frame


        # set default values


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")



app = App()
app.mainloop()
input()