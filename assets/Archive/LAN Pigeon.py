import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import threading
import ipaddress
import platform
import socket
import subprocess
import urllib.request
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from datetime import datetime
from PIL import Image

import customtkinter
from customtkinter import CTkImage
import sys
import winreg
import os

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Global Variables
currentDateAndTime = datetime.now()
currentTime = currentDateAndTime.strftime("%d/%m/%Y %H:%M:%S")
scan_in_progress = False
stop_scan = False
socket.setdefaulttimeout(0.350)

# Download the icon from the GitHub repository
url_light = "https://github.com/Perrtyk/python/blob/main/Testing/LAN%20Pigeon/Assets/icon_light.png?raw=true"
url_dark = "https://github.com/Perrtyk/python/blob/main/Testing/LAN%20Pigeon/Assets/icon_dark.png?raw=true"
url_bit = "https://github.com/Perrtyk/python/blob/main/Testing/LAN%20Pigeon/Assets/bit_icon.png?raw=true"
urllib.request.urlretrieve(url_light, "icon_light.png")
urllib.request.urlretrieve(url_dark, "icon_dark.png")
urllib.request.urlretrieve(url_bit, "bit_icon.png")
bit_icon = Image.open("bit_icon.png")
bit_icon.save("bit_icon.ico")
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("LAN Pigeon.py")
        self.geometry(f"{1200}x{600}")
        self.minsize(900, 600)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((1, 2), weight=1)

        # Create a menu bar
        menu_bar = tk.Menu(self, bg="#20232A")
        menu_bar.configure(bg='blue')
        self.configure(menu=menu_bar)

        # Create a "File" menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.configure(background='light grey')
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Create a "Help" menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.configure(background='light grey')
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="LAN Pigeon",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.iconbitmap("bit_icon.ico")
        icon_light = Image.open("icon_light.png")
        icon_dark = Image.open("icon_dark.png")
        self.logo_icon = customtkinter.CTkImage(light_image=icon_light,
                                                dark_image=icon_dark,
                                                size=(150, 115))
        self.icon_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_icon, anchor=tkinter.CENTER, text='')
        self.icon_label.grid(row=1, column=0, padx=10, pady=(10, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Start Scan", command=lambda: threading.Thread (target=self.scan_ip_range, args=(self.start_entry.get(), self.end_entry.get(), self.progress_var)).start())
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stop Scan",
                                                        command=self.stop_scan_func)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Save Results",
                                                        command=self.save_results)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:",
                                                            anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # create center frame
        self.main_entry_frame = customtkinter.CTkFrame(self)
        self.main_entry_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.main_entry_frame.columnconfigure((1, 2, 3, 4), weight=1)
        self.main_entry_frame.grid_rowconfigure(0, weight=0)
        self.main_entry_frame.grid_rowconfigure(1, weight=0)
        self.main_entry_frame.grid_rowconfigure(2, weight=1)
        self.main_entry_frame.grid_rowconfigure(3, weight=0)
        self.main_entry_frame.grid_rowconfigure(4, weight=1)

        # row 0
        self.label_start_scan = customtkinter.CTkLabel(master=self.main_entry_frame, text="Start Scan IP:",
                                                       font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label_start_scan.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.start_entry = customtkinter.CTkEntry(self.main_entry_frame, placeholder_text="192.168.0.1")
        self.start_entry.grid(row=0, column=1, padx=(0, 20), pady=(10, 10), sticky="nsew")
        self.label_end_scan = customtkinter.CTkLabel(master=self.main_entry_frame, text="End Scan IP:",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label_end_scan.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.end_entry = customtkinter.CTkEntry(self.main_entry_frame, placeholder_text="192.168.0.254")
        self.end_entry.grid(row=0, column=3, padx=(0, 20), pady=(10, 10), sticky="nsew")

        # row 1 and 2
        # Create the results treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#333", foreground="#fff", fieldbackground="#333")
        self.style.map("Treeview", background=[("selected", "#444")])
        self.style.configure('Treeview.Heading', background="#444", foreground="#fff")
        self.label_treeview = customtkinter.CTkLabel(master=self.main_entry_frame, width=250, text="Results",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label_treeview.grid(row=1, column=0, columnspan=4, rowspan=1, padx=(10, 0),
                                 pady=(10, 0), sticky='new')
        self.results_columns = ('IP Address', 'Hostname', 'MAC Address', 'Ping', 'Connectivity')
        self.results_treeview = ttk.Treeview(self.main_entry_frame, columns=self.results_columns,
                                             show='headings')
        self.results_treeview.grid(row=2, column=0, columnspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Configure the results treeview columns
        for column in self.results_columns:
            self.results_treeview.heading(column, text=column)
            self.results_treeview.column(column, anchor='center')
            self.results_treeview.column(column, width=150)

        # Create a scrollbar for the results treeview
        self.results_scrollbar = ttk.Scrollbar(self.main_entry_frame, orient='vertical', command=self.results_treeview.yview)
        self.results_scrollbar.grid(column=3, row=2, padx=(20, 0), pady=(20, 0), sticky="nse")
        self.results_treeview.configure(yscrollcommand=self.results_scrollbar.set)

        # row 3 - add code for this row later
        # Create the output console
        self.console_output = customtkinter.CTkTextbox(self.main_entry_frame, width=250)
        self.console_output.configure(font=('Consolas', 12, 'bold'))
        self.console_output.grid(row=3, column=0, columnspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # row 4 - add progress bar from its frame
        self.progress_var = tk.DoubleVar()
        self.progressbar_1 = customtkinter.CTkProgressBar(self.main_entry_frame)
        self.progressbar_1.grid(row=4, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ews")
        self.main_entry_frame.grid_rowconfigure(4, weight=0)
        self.percentage_label = customtkinter.CTkLabel(self.main_entry_frame, text='', anchor=tk.CENTER)
        self.percentage_label.grid(row=5, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ews")

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Ping Threshold",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="ew")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="  25ms",
                                                           variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="w")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="  50ms",
                                                           variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="w")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="  100ms",
                                                           variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="w")
        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="  250ms",
                                                           variable=self.radio_var, value=3)
        self.radio_button_4.grid(row=4, column=2, pady=10, padx=20, sticky="w")

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(master=self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(5, 0), sticky="nsew")
        self.label_checkbox_group = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text="Options",
                                                           font=customtkinter.CTkFont(size=14, weight="bold"))
        self.label_checkbox_group.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="ew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Mac Address")
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Host Name")
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="w")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Ping")
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="w")

        self.exit_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", text="Exit",
                                                     border_width=2, text_color=("gray10", "#DCE4EE"),
                                                     command=self.exit)
        self.exit_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # set default values
        start, end = '192.168.1.1', '192.168.1.254'
        self.start_entry.insert(0, f"{start}") # this will have user's subnet in the end
        self.end_entry.insert(0, f"{end}") # this will have user's subnet in the end
        self.sidebar_button_2.configure(state="normal")
        self.sidebar_button_3.configure(state="disabled")
        self.radio_button_1.configure(state="disabled")
        self.radio_button_2.configure(state="disabled")
        self.radio_button_3.configure(state="disabled")
        self.radio_button_4.configure(state="disabled")
        self.checkbox_1.configure(state="disabled")
        self.checkbox_2.configure(state="disabled")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.checkbox_2.select()
        self.checkbox_3.select()
        self.radio_button_3.select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.progressbar_1.configure(mode="indeterminnate", progress_color="green")
        self.progressbar_1.start()
        self.console_output.insert("0.0", "Console\n\n")

    # Prints debug command in both terminals. Updates the currentTime variable to reflect most recent time.
    def print_debug(self, msg):
        global currentTime
        currentTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(msg)
        self.console_output.insert(tk.END, msg + '\n')
        self.console_output.see(tk.END)

    def get_ping(self, ip_address):
        if stop_scan:
            ping_time = 'N/A'
            return ping_time
        self.print_debug(f'[{currentTime}] IP Scan ({ip_address}): Running PING process . . .\n')
        ping_response = subprocess.Popen(['ping', '-n', '3', '-w', '350', ip_address],
                                         stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
        if b'Reply from' in ping_response:
            ping_time = str(ping_response).split("Average =")[1].split("ms")[0] + ' ms'
            self.print_debug(f'[{currentTime}] IP Scan ({ip_address}): Received ping response of{ping_time}.\n')
            return ping_time
        else:
            ping_time = 'Request timed out.'
            return ping_time

    # Define the function to check whether an IP address is available
    def check_ip_address(self, ip_address):
        message_connect = f'[{currentTime}] Connect ({ip_address}):'
        self.print_debug(f'{message_connect} Running connection test . . .\n')
        response = subprocess.Popen(['ping', '-n', '1', '-w', '350', str(ip_address)],
                                    stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
        available, not_available = 'Yes', 'No'
        if b'Reply from' in response:
            if stop_scan:
                result = f'{not_available}'
                self.print_debug(f'{message_connect} Complete, endpoint available: {result}.\n')
                return result
            else:
                result = f'{available}'
                self.print_debug(f'{message_connect} Complete, endpoint available: {result}.\n')
                return result
        else:
            result = f'{not_available}'
            self.print_debug(f'{message_connect} Complete, endpoint available: {result}.\n')
            return result

    def get_mac_address(self, ip_address):
        self.print_debug(f'[{currentTime}] IP Scan ({ip_address}): Running MAC address process . . .\n')
        message_mac = f'[{currentTime}]     MAC ({ip_address}):'
        if stop_scan:
            mac_address = 'N/A'
            return mac_address
        elif not stop_scan:
            # Create an ARP request packet for the given IP address
            self.print_debug(f'{message_mac} Attempting to gather MAC address via ARP . . .\n')
            arp_request = ARP(pdst=ip_address)

            # Create an Ethernet frame with the broadcast destination MAC address
            ether = Ether(dst='ff:ff:ff:ff:ff:ff')

            # Combine the ARP request packet and Ethernet frame
            packet = ether / arp_request

            try:
                # Send the packet and receive the response
                self.print_debug(f'{message_mac} Sending out packet and awaiting response . . .\n')
                result = srp(packet, timeout=3, verbose=0)[0]

                # Extract the MAC address from the response
                mac_address = result[0][1].hwsrc
                self.print_debug(f'{message_mac} Extracting MAC from response . . .\n')
            except IndexError:
                # Return 'N/A' if an index error occurs
                self.print_debug(f'{message_mac} Index error, return N/A . . .\n')
                mac_address = 'N/A'
            self.print_debug(f'{message_mac} Returned MAC address . . .\n')
            return mac_address
        else:
            mac_address = 'N/A'
            self.print_debug(f'{message_mac} Endpoint unavailable . . .\n')
            return mac_address

    def get_host_name(self, ip_address):
        self.print_debug(f'[{currentTime}] IP Scan ({ip_address}): Gathering hostname . . .\n')
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            self.print_debug(f'[{currentTime}] IP Scan ({ip_address}): Hostname is {hostname}\n')
            return hostname
        except socket.herror as e:
            self.print_debug(f'[{currentTime}] IP Scan ({ip_address}): Error resolving hostname: {e}\n')
            hostname = 'N/A'
            return hostname
        except Exception as e:
            self.print_debug(f'[{currentTime}] IP Scan ({ip_address}): Error: {e}\n')
            hostname = 'N/A'
            return hostname

    # Define the function to scan a range of IP addresses and display the results in a table
    def scan_ip_range(self, start_ip, end_ip, progress_var):
        # Initialize stop scan variable
        global stop_scan, scan_in_progress
        stop_scan = False
        scan_in_progress = True
        self.disable_scan_button()
        self.progressbar_1.stop()
        self.progressbar_1.set(0)
        self.progressbar_1.configure(mode="determinate", progress_color="green")
        # Clear the existing rows in the treeview
        self.print_debug(f'[{currentTime}] IP Scan: scan_ip_range . . .\n')
        for row in self.results_treeview.get_children():
            self.results_treeview.delete(row)
        self.print_debug(f'[{currentTime}] IP Scan: Clearing existing rows.\n')

        # Set the maximum value for the progress bar
        progress_var.set(0)
        try:
            max_val = int(ipaddress.ip_address(end_ip)) - int(ipaddress.ip_address(start_ip))
        except ValueError as e:
            self.print_debug(f'[{currentTime}] IP Scan: {e}.\n')
            self.stop_scan_func()

        if max_val == 0:
            max_val = 1

        # Loop through the IP addresses in the range

        for i in range(int(ipaddress.ip_address(start_ip)), int(ipaddress.ip_address(end_ip)) + 1):
            if stop_scan:
                self.print_debug(f'[{currentTime}] Scan stopped.')
                break

            ip_address = str(ipaddress.ip_address(i))
            percentage = int((i - int(ipaddress.ip_address(start_ip))) * 100 / max_val)
            self.progressbar_1.set(percentage * .01)
            self.percentage_label.configure(text=f'{percentage}% | Scanning: {ip_address}')
            available = self.check_ip_address(ip_address)
            if available == 'No':
                self.print_debug(f'[{currentTime}] IP Scan ({ip_address}): Skipping, host is not available.\n')
                progress_var.set(progress_var.get() + 1)
                continue
            else:
                mac_address = self.get_mac_address(ip_address)

                ping_time = self.get_ping(ip_address)

                hostname = self.get_host_name(ip_address)

                progress_var.set(progress_var.get() + 1)

                self.print_debug(f"[{currentTime}] Processed IP Address: {ip_address} , Processed Ping: {ping_time}"
                            f" , Processed Hostname: {hostname}\n"
                            f"[{currentTime}] Processed MAC: {mac_address} ,"
                            f"Processed Connectivity: {available}\n")

                # Add a row to the treeview with the IP address, hostname, MAC address, ping time, and availability
                self.results_treeview.insert('', 'end', values=(ip_address, hostname, mac_address, ping_time, available))

        else:
            self.progressbar_1.set(0)
            self.progressbar_1.configure(mode="indeterminnate", progress_color="green")
            self.progressbar_1.start()
            self.print_debug(f'[{currentTime}] Scan completed.')
            scan_in_progress = False
            self.enable_scan_button()

    # Define the function to stop the scan
    def stop_scan_func(self):
        global stop_scan, scan_button
        self.sidebar_button_1.configure(state="normal", text="Scan")
        stop_scan = True

    def disable_scan_button(self):
        global scan_in_progress, scan_button
        scan_in_progress = True
        self.sidebar_button_1.configure(state="disabled", text="Scanning...")

    def enable_scan_button(self):
        global scan_in_progress, scan_button
        scan_in_progress = False
        self.sidebar_button_1.configure(state="normal", text="Scan")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def get_os_dark_mode(self):
        if sys.platform == "win32":
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                print(value)
                return "Light" if value == 1 else "Dark"
            except:
                return None
        elif sys.platform == "darwin":
            try:
                cmd = "defaults read -g AppleInterfaceStyle"
                output = subprocess.check_output(cmd, shell=True)
                print(output)
                return "Light" if output.strip() == b'Light' else "Dark"
            except:
                return None
        elif sys.platform.startswith("linux"):
            try:
                cmd = "gsettings get org.gnome.desktop.interface gtk-theme"
                output = os.popen(cmd).read()
                print(output)
                return "Light" if "Adwaita" in output else "Dark"
            except:
                return None
        else:
            return None

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode.lower() == "light":
            self.treeview_light()
        elif new_appearance_mode.lower() == "dark":
            self.treeview_dark()
        else:
            if self.get_os_dark_mode().lower() == "light":
                self.treeview_light()
            else:
                self.treeview_dark()
        # get current treeview data
        treeview_data = []
        for child in self.results_treeview.get_children():
            treeview_data.append(self.results_treeview.item(child)['values'])

        # save properties of the old treeview
        treeview_style = self.results_treeview.cget("style")
        treeview_width = self.results_treeview.winfo_width()
        treeview_height = self.results_treeview.winfo_height()

        # destroy old treeview
        self.results_treeview.destroy()

        # create new treeview with updated style
        self.results_treeview = ttk.Treeview(self.main_entry_frame, columns=self.results_columns, show='headings',
                                             style=treeview_style)
        self.results_treeview.grid(row=2, column=0, columnspan=4, padx=(20, 0), pady=(20, 0), sticky="new")

        # set size of the new treeview to match the old one
        for idx, column in enumerate(self.results_columns):
            self.results_treeview.column(column, width=treeview_width)
        self.results_treeview.configure(height=treeview_height)

        # configure the columns of the new treeview
        for column in self.results_columns:
            self.results_treeview.heading(column, text=column)
            self.results_treeview.column(column, anchor='center')
            self.results_treeview.column(column, width=150)

        # add data to the new treeview
        for data in treeview_data:
            self.results_treeview.insert('', 'end', values=data)

        # re-adjust the scrollbar to match new data
        self.results_scrollbar.destroy()
        self.results_scrollbar = ttk.Scrollbar(self.main_entry_frame, orient='vertical', command=self.results_treeview.yview)
        self.results_scrollbar.grid(column=3, row=2, padx=(20, 0), pady=(20, 0), sticky="nse")
        self.results_treeview.configure(yscrollcommand=self.results_scrollbar.set)

    def treeview_light(self):
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#fff", foreground="#000", fieldbackground="#fff")
        self.style.map("Treeview", background=[("selected", "#eee")])
        self.style.configure('Treeview.Heading', background="#ccc", foreground="#000")

    def treeview_dark(self):
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#333", foreground="#fff", fieldbackground="#333")
        self.style.map("Treeview", background=[("selected", "#444")])
        self.style.configure('Treeview.Heading', background="#444", foreground="#fff")

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def start_scan_botton(self):
        print("start scan click")

    def stop_scan_botton(self):
        print("stop scan click")

    def save_results(self):
        print("save_results button press")

    def exit(self):
        return exit()


if __name__ == "__main__":
    app = App()
    app.mainloop()