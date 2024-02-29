import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox, font, ttk
import customtkinter
from PIL import Image, ImageTk
import os
import server, client # import server.py and client.py

# create tkinter for --
#  1. upload files/folder and playback in order
#  2. change order?
#  3. control panel with functional buttons (area light, select and play)
#  4. Select device

class Local_File:
    def __init__(self):
        self.files = []

    def add_file(self, file_path):
        if os.path.exists(file_path):
            self.files.append(file_path)
            return True
        else:
            return False

    def delete_file(self, index):
        del self.files[index]

    def get_files(self):
        return self.files

class Cloud_File:
    def __init__(self):
        # Add: Show list of uploaded files. available for click and play
        self.files = []

    def add_file(self, file_path):
        if os.path.exists(file_path):
            self.files.append(file_path)
            return True
        else:
            return False

    def delete_file(self, index):
        del self.files[index]

    def get_files(self):
        return self.files

# Creating App class which will contain 
# Label Widgets 
class GUI: 
    def __init__(self, master) -> None: 
        self.root = root
        self.root.title("Smart Mirror Control Station")
        self.local_file = Local_File()
        self.cloud_file = Cloud_File()
        # self.server_socket = server.Server_Socket()
        # self.server_socket.connect_client()

        self.playing = False # initial state: all paused
        self.restart = False
        self.start_stream = False 
        self.img_path_list = ['assets/play-img.png','assets/start-img.png', 'assets/stream-img.png']
        self.img_list = []
        self.pb_buttons = []
        self.color = {
            "rose" : "#C77C78",
            "blue" : "#59BACC",
            "green" : "#58AD69", 
            "orange" : "#FFBC49",
            "red" : "#E2574C"
        }
        
        self.load_images()
        self.manage_file_ui()
        self.playback_ui()
        self.control_ui()

    def load_images(self):
        for path in self.img_path_list:
            btn_image = ImageTk.PhotoImage(Image.open(path).resize((20, 20), Image.LANCZOS))
            self.img_list.append(btn_image)
        self.pause_img = ImageTk.PhotoImage(Image.open('assets/pause-img.png').resize((20, 20), Image.LANCZOS))

    def manage_file_ui(self):
        self.section1 = tk.Frame(self.root)
        self.section1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame1 = tk.Frame(self.section1)
        # self.frame1.grid(row=0, column=0,pady=20, padx=20, sticky='nswe')
        self.frame1.pack(pady=20, padx=20, side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.title_font = tk.font.Font(size=20)
        self.manage_title = tk.Label(self.frame1, text="Manage File", font=self.title_font)
        self.manage_title.pack(side=tk.TOP)
        self.instructions = tk.Label(self.frame1, text="Click the button below to upload files")
        self.instructions.pack(padx=20, side=tk.TOP, anchor="nw")

        # self.entry = tk.Entry(self.frame, width=50)
        # self.entry.pack(side=tk.LEFT)

        self.action_frm = tk.Frame(self.frame1)
        self.action_frm.pack(padx=10, side=tk.TOP, anchor='nw')
        # self.browse_button = tk.Button(self.action_frm, text="Browse", command=self.browse_files)
        self.browse_button = customtkinter.CTkButton(self.action_frm, 
                                                        text="Browse", 
                                                        cursor="hand2", 
                                                        command=self.browse_files, 
                                                        text_color="#000000", 
                                                        fg_color="transparent", 
                                                        hover_color=self.color["orange"], 
                                                        border_width=1)
        self.browse_button.pack(pady=10, padx=10, side=tk.LEFT)
        # self.remove_button = tk.Button(self.action_frm, text="Remove", command=self.remove_file)
        self.remove_button = customtkinter.CTkButton(self.action_frm, 
                                                        text="Remove", 
                                                        cursor="hand2", 
                                                        command=self.remove_file, 
                                                        text_color="#000000", 
                                                        fg_color="transparent", 
                                                        hover_color=self.color["orange"], 
                                                        border_width=1)
        self.remove_button.pack(pady=10, padx=10,side=tk.LEFT)

        self.files_frm = tk.Frame(self.frame1)
        self.files_frm.pack(pady=20, padx=20, side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.added_files_frm = tk.Frame(self.files_frm)
        self.added_files_frm.pack(pady=20, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.added_files_label = tk.Label(self.added_files_frm, text="Media Files Added. Click on > to upload")
        self.added_files_label.pack()
        self.listbox_added = tk.Listbox(self.added_files_frm, width=50, selectmode = "multiple")
        self.listbox_added.pack(pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_added_scroll = ttk.Scrollbar(self.added_files_frm, style="Vertical.TScrollbar")
        self.list_added_scroll.pack(side=tk.RIGHT, fill=tk.Y) 
        self.listbox_added.config(yscrollcommand=self.list_added_scroll.set) 
        self.list_added_scroll.config(command=self.listbox_added.yview) 

        self.send_remove_frm = tk.Frame(self.files_frm)
        self.send_remove_frm.pack(side=tk.LEFT)
        self.send_button = tk.Button(self.send_remove_frm, text="Send File to Server", command=self.ready_to_send)
        self.send_button.pack(pady=10)
        self.delete_button = tk.Button(self.send_remove_frm, text="Remove from server", command=self.delete_file)
        self.delete_button.pack(pady=10)

        self.cloud_files_frm = tk.Frame(self.files_frm)
        self.cloud_files_frm.pack(pady=20, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.cloud_files_label = tk.Label(self.cloud_files_frm, text="Media Files Uploaded")
        self.cloud_files_label.pack()
        self.listbox_cloud = tk.Listbox(self.cloud_files_frm, width=50, selectmode = "multiple")
        self.listbox_cloud.pack(pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_cloud_scroll = ttk.Scrollbar(self.cloud_files_frm, style="Vertical.TScrollbar")
        self.list_cloud_scroll.pack(side=tk.RIGHT, fill=tk.Y) 
        self.listbox_cloud.config(yscrollcommand=self.list_cloud_scroll.set) 
        self.list_cloud_scroll.config(command=self.listbox_cloud.yview)

    def browse_files(self):
        filetype = (('video files', '*.mp4'),
                 ('image files', '*.png *.jpeg *.jpg'),
                 ('all files', '*.*')
                )
        # multiple file selections (single file: fd.askopenfilename())
        file_paths = fd.askopenfilenames(title="Select File(s)",
                                        filetypes=filetype,
                                        defaultextension='*.*')
        if file_paths:
            # save files to local_file and insert to listbox
            for file_path in file_paths:
                if self.local_file.add_file(file_path): # True if file_path appended to local_file 
                    self.listbox_added.insert(tk.END, file_path)
            self.instructions.configure(text="File(s) added to the list. ", fg="darkviolet") # for multi file selection
            
        # Below lines used when a Entry box needed
        # self.entry.delete(0, tk.END)
        # self.entry.insert(tk.END, filename)

    def remove_file(self):
        # Remove from local storage
        select_indices = self.listbox_added.curselection()
        if select_indices:
            for index in reversed(select_indices):
                # Ensure index is within valid range
                if 0 <= index < self.listbox_added.size():
                    self.listbox_added.delete(index) # Delete from listbox
                    self.local_file.delete_file(index) # Delete from storage            
            self.instructions.configure(text="File removed from the storage. ",fg="darkviolet")
        else:
            messagebox.showwarning("Warning", "Please select a file to remove!")
        
    # Select file from added list and send to server
    def ready_to_send(self):
        select_indices = self.listbox_added.curselection()
        if select_indices:
            for index in select_indices: 
                file_path = self.local_file.get_files()[index]
            
                if self.cloud_file.add_file(file_path): # True if file_path appended to cloud_file 
                    self.listbox_cloud.insert(tk.END, file_path)
                    # update playback list
                    file_name, file_type = self.get_filename_ext(file_path, index) # shortened to filename.ext
                    self.pb_list.insert(tk.END, f"{file_name}{file_type}")
                else:
                    messagebox.showwarning("Warning", "File did not send!")

            self.instructions.configure(text="File(s) sent to the device. ",fg="darkviolet")
        else:
            messagebox.showwarning("Warning", "Please select a file to send!")

    # Add: move selected files from right listbox to left listbox
    def delete_file(self):
        # Remove from cloud storage
        select_indices = self.listbox_cloud.curselection()
        if select_indices:
            for index in reversed(select_indices):
                # Ensure index is within valid range
                if 0 <= index < self.listbox_cloud.size():
                    self.listbox_cloud.delete(index)  # Delete from cloud listbox
                    self.cloud_file.delete_file(index)  # Delete from cloud_file
                    self.pb_list.delete(index)  # Delete from playback list
            self.instructions.configure(text="File removed from device. ", fg="darkviolet")
        else:
            messagebox.showwarning("Warning", "Please select a file to remove from uploads!")

    def get_filename_ext(self, file_path, index):
        # Extract file names and extensions from paths
        file_name = os.path.basename(file_path)
        file_name, file_type = os.path.splitext(file_name)
        return file_name, file_type
        
    def playback_ui(self):
        self.frame2 = tk.Frame(self.section1)
        self.frame2.pack(pady=20, padx=20, side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.playback_title = tk.Label(self.frame2, text="Select file and click an action button.")
        self.playback_title.pack(padx=20, side=tk.TOP, anchor='nw')
        
        # Key descriptions
        keys_list = """Keyboard:\n \'s\' for stop\n \'q\' for black screen\n \'p\' for resume to last play"""
        self.keys_usage = tk.Label(self.frame2, text=keys_list, justify=tk.LEFT)
        self.keys_usage.pack(padx=20, side=tk.TOP, anchor='nw')

        self.pb_list_frm = tk.Frame(self.frame2)
        self.pb_list_frm.pack(padx=20, side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Listbox properties
        self.pb_list = tk.Listbox(self.pb_list_frm, 
                                  borderwidth=0, 
                                  highlightthickness=0, # remove listbox border
                                  relief=tk.FLAT, # Default: SUNKEN
                                  selectbackground="darkviolet", # Font color
                                  cursor="hand2") 
        self.pb_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pb_scroll = ttk.Scrollbar(self.pb_list_frm, style="Vertical.TScrollbar") # Define scrollbar
        self.pb_scroll.pack(side=tk.RIGHT, fill=tk.Y) 
        self.pb_list.config(yscrollcommand=self.pb_scroll.set)  # Link scrollbar with listbox
        self.pb_scroll.config(command=self.pb_list.yview) # Scrollability

        self.status = tk.Label(self.frame2, text="<Nothing playing>", fg="darkviolet")
        self.status.pack(padx=20, side=tk.TOP, anchor="nw")
        
        self.btn_frm = tk.Frame(self.frame2)
        self.btn_frm.pack(padx=10, side=tk.TOP, anchor='nw', fill=tk.NONE)

        btn_text = ["Pause", "Play selection", "Camera"]
        self.btn_cmds =[self.pause_resume_cmd, self.restart_cmd, self.stream_cmd]
        # create playback buttons
        for txt, img, cmd in zip(btn_text, self.img_list, self.btn_cmds):
            button = customtkinter.CTkButton(self.btn_frm, 
                                            text=txt, 
                                            image=img, 
                                            cursor="hand2", 
                                            command=cmd, 
                                            text_color="#000000", 
                                            fg_color="transparent", 
                                            hover_color=self.color["orange"], 
                                            border_width=1,
                                            border_spacing=0)
            button.pack(pady=10, padx=10, side=tk.LEFT)
            self.pb_buttons.append(button)

        self.pb_buttons[0].configure(state="disabled") # disable pause/resume button
        self.pb_buttons[1].configure(state="disabled") # disable restart button
        self.pb_init()

    def pb_init(self):
        selection = self.pb_list.curselection()
        if selection:
            self.pb_buttons[0].configure(state="enabled") # disable pause/resume button
            self.pb_buttons[1].configure(state="enabled") # disable restart button
            # if self.status.cget("text") == "<Nothing playing>": # if text attribute of the label self.status is nothing playing
            index = selection[0]
            file_path = self.pb_list.get(index)
            if self.restart == True:
                self.status.configure(text=(f"Playing {self.pb_list.curselection()} from the beginning"))
                self.restart == False # set it as unclicked
            elif self.start_stream == True:
                self.status.configure(text=(f"Connecting camera to device (IP: [IP_addr])"))
                self.start_stream == False
                
                
    # self.pb_buttons[0]
    def pause_resume_cmd(self):
        if !self.playing:
            self.pb_buttons[0].configure(image=self.img_list[0],text="Resume")
            self.playing = True
            # send pause command to server
        else:
            self.pb_buttons[0].configure(image=self.pause_img,text="Pause")
            self.playing = False
            # send resume command to server 

    # self.pb_buttons[1]
    def restart_cmd(self):
        self.restart = True
        # restart the selected video
      
    # self.pb_buttons[2]
    def stream_cmd(self):
        self.start_stream = True
        file_path = 0 # will connect the camera
        # send file_path to the client
    
    def control_ui(self):
        self.section2 = tk.Frame(self.root)
        self.section2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame3 = tk.Frame(self.section2)
        self.frame3.pack(pady=20, padx=20, side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.ctrl_title = tk.Label(self.frame3, text="Control Panel", font=self.title_font)
        self.ctrl_title.pack(side=tk.TOP)
        self.ctrl_inst = tk.Label(self.frame3, text="Click on button to enable")
        self.ctrl_inst.pack(padx=20, side=tk.TOP, anchor='nw')
        
        self.ctrl_btn_frm = tk.Frame(self.frame3)
        self.ctrl_btn_frm.pack(side=tk.TOP)
        self.L_light = tk.Button(self.ctrl_btn_frm, text="Left light")
        self.L_light.pack(side=tk.LEFT, padx=20, pady=20)
        self.C_light = tk.Button(self.ctrl_btn_frm, text="Center light")
        self.C_light.pack(side=tk.LEFT, padx=20, pady=20)
        self.R_light = tk.Button(self.ctrl_btn_frm, text="Right light")
        self.R_light.pack(side=tk.LEFT, padx=20, pady=20)

# # Frame--select device
# device_frm = tk.Frame(window, width=180, height=100)
# # device_frm.columnconfigure(0, minsize=250)
# # device_frm.rowconfigure([0, 1], minsize=100)
# device_frm.pack()
# select_label = tk.Label(device_frm, text="Choose the device to control", font=20).grid(row=0, column=0, sticky="w")
# device1 = tk.Button(device_frm, text="device name 1").grid(row=1, column=0) # Receive device names from the same network
# device2 = tk.Button(device_frm, text="device name 2").grid(row=2, column=0) # Receive device names from the same network


# # Frame 2--change playback order
# order_frm = tk.Frame(master=window) 
# order_frm.pack(fill=tk.Y, side=tk.RIGHT, expand=True)
# order_title = tk.Label(order_frm, text="Media added", font=20).pack(padx=20, pady=10)
# order_des = tk.Label(order_frm, text="Click to instant play or move items to change the order").pack()
# # list_frm = tk.Frame(order_frm)
# # list_frm.pack(side=tk.LEFT)
        
    

if __name__ == "__main__": 
  
    # Instantiating top level 
    root = tk.Tk() 
  
    # Setting the title of the window 
    root.title("Smart Mirror") 

    # check default font
    # print(font.nametofont('TkDefaultFont').actual())
  
    # Setting the geometry i.e Dimensions 
    # root.geometry("400x250") 
  
    # Calling our App 
    gui = GUI(root) 
  
    # Mainloop which will cause this toplevel 
    # to run infinitely 
    root.mainloop() # Start the application. listens for event (loop)
