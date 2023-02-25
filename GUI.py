import tkinter as tk
import time

# ADMIN ELEVATION
import pyuac

# COMPUTER RENAME
from menu_change_name import change_computer_name
import platform
import subprocess

# IP ADDRESS CHANGE
from menu_change_ip import get_network_adapters
from menu_change_ip import change_network_adapters

# SOFTWARE DONWLOAD
from menu_download_software import get_download

# APPLICATION LIST
from application_list import APPLICATION_DOWNLOAD_LIST

class MyApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.bg_color = "#000041"
        self.root.configure(bg=self.bg_color)

        # --------------------------------- MAIN MENU -------------------------------- #
        self.main_menu = tk.Frame(root)
        self.create_widgets_main_menu()
        # ------------------------------- COMPUTER NAME ------------------------------ #
        self.computer_name_menu = tk.Frame(root)
        self.create_widgets_computer_name()
        # ----------------------------- IP ADDRESS CHANGE ---------------------------- #
        self.ip_address_menu = tk.Frame(root)
        self.ip_address_change_menu = tk.Frame(root)
        self.create_widgets_ip_address()
        # ----------------------------- SOFTWARE DOWNLOAD ---------------------------- #
        self.software_download_menu = tk.Frame(root)
        self.software_download_options_menu = tk.Frame(root)
        self.create_widgets_software_download()
        self.create_widgets_software_options_download()


# ---------------------------------------------------------------------------- #
#                                   MAIN MENU                                  #
# ---------------------------------------------------------------------------- #


    def create_widgets_main_menu(self):

         # Create widgets for main_menu
        self.main_menu_widgets = []
        self.main_menu_widgets.append(tk.Label(self.main_menu, text="TCBatch", font=("TkDefaultFont", 24), width=10, bg="black", fg="white"))
        self.main_menu_widgets.append(tk.Button(self.main_menu, text="Change Computer Name", command=self.show_computer_name_menu, font=('TkDefaultFont', 12), borderwidth=3, width=20, activebackground="green", bg="black", fg="white"))
        self.main_menu_widgets.append(tk.Button(self.main_menu, text="Change IP Addresses", command=self.show_ip_address_menu, font=('TkDefaultFont', 12), borderwidth=3, width=20, activebackground="green", bg="black", fg="white"))
        self.main_menu_widgets.append(tk.Button(self.main_menu, text="Download Software", command=self.show_software_download_menu, font=('TkDefaultFont', 12), borderwidth=3, width=20, activebackground="green", bg="black", fg="white"))
        self.main_menu_widgets.append(tk.Button(self.main_menu, text="Install Software", command=self.show_main_menu, font=('TkDefaultFont', 12), borderwidth=3, width=20, activebackground="green", bg="black", fg="white"))
        self.main_menu_widgets.append(tk.Button(self.main_menu, text="Create Symlink Folder", command=self.show_main_menu, font=('TkDefaultFont', 12), borderwidth=3, width=20, activebackground="green", bg="black", fg="white"))
        self.main_menu_widgets.append(tk.Button(self.main_menu, text="Restart Computer", command=self.show_main_menu, font=('TkDefaultFont', 12), borderwidth=3, width=20, activebackground="green", bg="black", fg="white"))
        
        for i, widget in enumerate(self.main_menu_widgets):
            widget.grid(row=i,column=0)

# ---------------------------------------------------------------------------- #
#                             COMPUTER RENAME MENU                             #
# ---------------------------------------------------------------------------- #
        
    def create_widgets_computer_name(self):
    
        # ------------------------------- DEFINE WIDGETS ------------------------------ #
        self.computer_name_label_title = tk.Label(self.computer_name_menu, text="CHANGE COMPUTER NAME", font=("TkDefaultFont", 24), bg="black", fg="white")
        self.computer_name_label_current = tk.Label(self.computer_name_menu, text="CURRENT COMPUTER NAME:", font=("TkDefaultFont", 12), bg=self.bg_color, fg="white")
        self.computer_name_label_name = tk.Label(self.computer_name_menu, text=platform.node(), font=("TkDefaultFont", 12), bg=self.bg_color, fg="white")
        self.computer_name_label_spacer1 = tk.Label(self.computer_name_menu, text="", bg=self.bg_color, font=("TkDefaultFont", 12))
        self.computer_name_entry_name = tk.Entry(self.computer_name_menu, font=("TkDefaultFont", 18), width=30)
        self.computer_name_label_spacer2 = tk.Label(self.computer_name_menu, text="", bg=self.bg_color, font=("TkDefaultFont", 12))
        self.computer_name_button_cancel = tk.Button(self.computer_name_menu, text="CANCEL", command=self.show_main_menu, borderwidth=3, width=20, activebackground="green", bg="black", fg="white")
        self.computer_name_button_enter = tk.Button(self.computer_name_menu, text="ENTER", command=self.get_entry_computer_name_change, borderwidth=3, width=20, activebackground="green", bg="black", fg="white")

        # ------------------------------- SHOW WIDGETS ------------------------------- #
        self.computer_name_label_title.grid(row=0,column=0,columnspan=2)
        self.computer_name_label_title.grid(row=1,column=0,columnspan=2)
        self.computer_name_label_current.grid(row=2,column=0,columnspan=2)
        self.computer_name_label_name.grid(row=3,column=0,columnspan=2)
        self.computer_name_label_spacer1.grid(row=4,column=0,columnspan=2)
        self.computer_name_entry_name.grid(row=5,column=0,columnspan=2)
        self.computer_name_label_spacer2.grid(row=6,column=0,columnspan=2)
        self.computer_name_button_cancel.grid(row=7,column=0)
        self.computer_name_button_enter.grid(row=7,column=1)



    def get_entry_computer_name_change(self):
        value = self.computer_name_entry_name.get()
        try:
            change_computer_name(value)
            self.computer_name_change_confirmation = "\nCHANGING COMPUTER NAME ON RESTART"
        except:
            self.computer_name_change_confirmation = "\nERROR, COULD NOT CHANGE NAME"

        self.computer_name_change_confirmation = tk.Label(self.computer_name_menu, text= self.computer_name_change_confirmation, font=("TkDefaultFont", 14), bg=self.bg_color, fg="red")
        self.computer_name_change_confirmation.grid(row=8,column=0,columnspan=2)


# ---------------------------------------------------------------------------- #
#                            IP ADDRESS CHANGE MENU                            #
# ---------------------------------------------------------------------------- #

    # --------------------------- MAIN IP ADDRESS MENU --------------------------- #
    def create_widgets_ip_address(self):

        interfaces = get_network_adapters()

        self.ip_address_menu_widgets = []
        self.ip_address_menu_widgets.append(tk.Label(self.ip_address_menu, text="CHANGE IP ADRESSES", font=("TkDefaultFont", 24), bg="black", fg="white"))

        for i, interface in enumerate(interfaces):
             self.ip_address_menu_widgets.append(tk.Button(self.ip_address_menu, text=interface, command=lambda i=i: self.create_widgets_ip_address_change(interfaces[i]), font=('TkDefaultFont', 12), borderwidth=3, width=30, activebackground="green", bg="black", fg="white"))

        for i, widget in enumerate(self.ip_address_menu_widgets):
            widget.grid(row=i,column=0)

    # --------------------- SECONDARY IP ADDRESS CHANGE MENU --------------------- #

    def create_widgets_ip_address_change(self, interface: str):
        self.show_ip_address_change_menu()

        # ------------------------------- DEFINE LABELS ------------------------------ #
        self.ip_address_change_label_title = tk.Label(self.ip_address_change_menu, text=interface, font=("TkDefaultFont", 24), width=20, bg="black", fg="white")
        self.ip_address_change_label_ip = tk.Label(self.ip_address_change_menu, text="IP ADDRESS", font=("TkDefaultFont", 12), width=20, bg=self.bg_color, fg="white")
        self.ip_address_change_label_subnet = tk.Label(self.ip_address_change_menu, text="SUBNET", font=("TkDefaultFont", 12), width=20, bg=self.bg_color, fg="white")
        self.ip_address_change_label_gateway = tk.Label(self.ip_address_change_menu, text="DEFAULT GATEWAY", font=("TkDefaultFont", 12), width=20, bg=self.bg_color, fg="white")
        self.ip_address_change_label_primary_dns = tk.Label(self.ip_address_change_menu, text="PREFERRED DNS", font=("TkDefaultFont", 12), width=20, bg=self.bg_color, fg="white")
        self.ip_address_change_label_secondary_dns = tk.Label(self.ip_address_change_menu, text="ALTERNATE DNS", font=("TkDefaultFont", 12), width=20, bg=self.bg_color, fg="white")

        # ---------------------------- DEFINE ENTRY BOXES ---------------------------- #
        self.ip_address_change_entry_ip = tk.Entry(self.ip_address_change_menu, font=("TkDefaultFont", 12), width=15)
        self.ip_address_change_entry_subnet = tk.Entry(self.ip_address_change_menu, font=("TkDefaultFont", 12), width=15)
        self.ip_address_change_entry_gateway = tk.Entry(self.ip_address_change_menu, font=("TkDefaultFont", 12), width=15)
        self.ip_address_change_entry_primary_dns = tk.Entry(self.ip_address_change_menu, font=("TkDefaultFont", 12), width=15)
        self.ip_address_change_entry_secondary_dns = tk.Entry(self.ip_address_change_menu, font=("TkDefaultFont", 12), width=15)

        # ---------------------------------- BUTTONS --------------------------------- #
        self.ip_address_change_button_cancel = tk.Button(self.ip_address_change_menu, text="CANCEL", command=self.show_ip_address_menu, borderwidth=3, width=20, activebackground="green", bg="black", fg="white")
        self.ip_address_change_button_enter = tk.Button(self.ip_address_change_menu, text="ENTER", command=lambda: self.get_entry_ip_address_changes(interface), borderwidth=3, width=20, activebackground="green", bg="black", fg="white")


        # ------------------------------- SHOW WIDGETS ------------------------------- #
        self.ip_address_change_label_title.grid(row=0,column=0,columnspan=2)

        self.ip_address_change_label_ip.grid(row=1,column=0)
        self.ip_address_change_entry_ip.grid(row=1,column=1)

        self.ip_address_change_label_subnet.grid(row=2,column=0)
        self.ip_address_change_entry_subnet.grid(row=2,column=1)

        self.ip_address_change_label_gateway.grid(row=3,column=0)
        self.ip_address_change_entry_gateway.grid(row=3,column=1)

        self.ip_address_change_label_primary_dns.grid(row=4,column=0)
        self.ip_address_change_entry_primary_dns.grid(row=4,column=1)

        self.ip_address_change_label_secondary_dns.grid(row=5,column=0)
        self.ip_address_change_entry_secondary_dns.grid(row=5,column=1)

        self.ip_address_change_button_cancel.grid(row=6,column=0)
        self.ip_address_change_button_enter.grid(row=6,column=1)

    def get_entry_ip_address_changes(self, interface: str):
         change_network_adapters(interface, self.ip_address_change_entry_ip.get(),self.ip_address_change_entry_subnet.get(),self.ip_address_change_entry_gateway.get(),self.ip_address_change_entry_primary_dns.get(),self.ip_address_change_entry_secondary_dns.get())


    # ---------------------------------------------------------------------------- #
    #                               SOFTWARE DOWNLOAD                              #
    # ---------------------------------------------------------------------------- #
    def create_widgets_software_download(self):
    # ------------------------------- DEFINE WIDGETS ------------------------------ #
        self.software_download_label_title = tk.Label(self.software_download_menu, text="SOFTWARE DOWNLOAD", font=("TkDefaultFont", 24), width=20, bg="black", fg="white").grid(row=0,column=0,columnspan=2)
        self.software_download_canvas = tk.Canvas(self.software_download_menu, height=350)
        self.software_download_scrollbar = tk.Scrollbar(self.software_download_menu, orient="vertical", command=self.software_download_canvas.yview)
        self.software_download_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.software_download_canvas_frame = tk.Frame(self.software_download_canvas)

        self.software_download_button_cancel = tk.Button(self.software_download_menu, text="CANCEL", command=self.show_ip_address_menu, borderwidth=3, width=20, activebackground="green", bg="black", fg="white").grid(row=2,column=0)
        self.software_download_button_enter = tk.Button(self.software_download_menu, text="ENTER", command=self.get_entry_software_downloads, borderwidth=3, width=20, activebackground="green", bg="black", fg="white").grid(row=2,column=1)

        # ------------------------------- SHOW WIDGETS ------------------------------- #
        self.software_download_canvas.grid(row=1,column=0,columnspan=2)
        self.software_download_scrollbar.grid(row=1, column=2, sticky='NS')
        self.software_download_canvas.configure(yscrollcommand=self.software_download_scrollbar.set)

        self.software_download_canvas.create_window((0,0), window=self.software_download_canvas_frame, anchor="nw")
        self.software_download_canvas_frame.bind("<Configure>", lambda event, canvas=self.software_download_canvas: self.onFrameConfigure(canvas))


        self.software_download_bools = [] # = tk.BooleanVar()

        # Add checkboxes to the canvas frame
        self.software_download_list = []
        for i, software in enumerate(APPLICATION_DOWNLOAD_LIST):
            if i % 2 == 0:
                self.list_color = "#0A0A0A"   
            else:
                self.list_color = "#2A2A2A"

            var = tk.BooleanVar()
            widget = tk.Checkbutton(self.software_download_canvas_frame, text=software.display, variable=var, font=("TkDefaultFont", 12), width=41, selectcolor="black", bg=self.list_color, fg="white", anchor='w').grid(row=i, column=0)
            self.software_download_list.append(widget)
            self.software_download_bools.append(var)

        # Set the scrollregion of the canvas
        self.software_download_canvas.configure(scrollregion=self.software_download_canvas.bbox('all'))




    def onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox('all'))

    def _on_mousewheel(self, event):
        self.software_download_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")


    def get_entry_software_downloads(self):
        active = []
        for i, var in enumerate(self.software_download_bools):
            if var.get():
                active.append(i)
        for i in active:
            # print(APPLICATION_DOWNLOAD_LIST[i])
            get_download(APPLICATION_DOWNLOAD_LIST[i], False)
            self.software_download_bools[i].set(False)  # clear the checkbox

    def create_widgets_software_options_download(self):
        pass



            
# ---------------------------------------------------------------------------- #
#                                   SHOW MENU                                  #
# ---------------------------------------------------------------------------- #
    
    # --------------------------------- MAIN MENU -------------------------------- #
    def show_main_menu(self):
        self.hide_all_menu()

        self.main_menu.configure(bg=self.bg_color)
        self.main_menu.pack(side="left",fill="both")
        self.root.geometry('200x250')
        
    # --------------------------- COMPUTER NAME CHANGE --------------------------- #
    def show_computer_name_menu(self):
        self.hide_all_menu()

        self.computer_name_menu.configure(bg=self.bg_color)
        self.computer_name_menu.pack(side="left",fill="both")
        self.root.geometry('630x250')

    # ----------------------------- IP ADDRESS CHANGE ---------------------------- #
    def show_ip_address_menu(self):
        self.hide_all_menu()

        self.ip_address_menu.configure(bg=self.bg_color)
        self.ip_address_menu.pack(side="left",fill="both")
        self.root.geometry('560x250')

    def show_ip_address_change_menu(self):

        self.ip_address_change_menu.configure(bg=self.bg_color)
        self.ip_address_change_menu.pack(side="left",fill="both")
        self.root.geometry('950x250')

    # ----------------------------- SOFTWARE DOWNLOAD ---------------------------- #
    def show_software_download_menu(self):
        self.hide_all_menu()

        self.software_download_menu.configure(bg=self.bg_color)
        self.software_download_menu.pack(side="left",fill="both")
        self.root.geometry('630x450')

    def show_software_download_options_menu(self):

        self.software_download_options_menu.configure(bg=self.bg_color)
        self.software_download_options_menu.pack(side="left",fill="both")
        self.root.geometry('950x450')


    
    def hide_all_menu(self):
        self.computer_name_menu.pack_forget()
        self.ip_address_menu.pack_forget()
        self.ip_address_change_menu.pack_forget()
        self.software_download_menu.pack_forget()
         
        

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #


def main():
    root = tk.Tk()
    app = MyApp(root)
    # Show main_menu initially
    app.show_main_menu()
    root.mainloop()




if __name__ == "__main__":
	if not pyuac.isUserAdmin():
		print("RE-LAUNCHING AS ADMIN!")
		time.sleep(1)
		pyuac.runAsAdmin()
	else:        
		main()  # Already an admin here.