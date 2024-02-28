import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox, font, ttk
import cv2
import socket
import pickle
import struct
import os

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

        self.manage_file_ui()
        self.playback_ui()
            
    def manage_file_ui(self):
        self.frame1 = tk.Frame(self.root)
        self.frame1.pack(pady=20, padx=20, side=tk.LEFT)

        self.title_font = tk.font.Font(size=20)
        self.manage_title = tk.Label(self.frame1, text="Manage File", font=self.title_font)
        self.manage_title.grid(row=0, column=0)
        self.instructions = tk.Label(self.frame1, text="Click the button below to upload files")
        self.instructions.grid(row=1, column=0, sticky="w")

        # self.entry = tk.Entry(self.frame, width=50)
        # self.entry.pack(side=tk.LEFT)

        self.action_frm = tk.Frame(self.frame1)
        self.action_frm.grid(row=2, column=0, sticky='w')
        self.browse_button = tk.Button(self.action_frm, text="Browse", command=self.browse_files)
        self.browse_button.pack(pady=10, side=tk.LEFT)
        self.remove_button = tk.Button(self.action_frm, text="Remove", command=self.remove_file)
        self.remove_button.pack(pady=10, side=tk.LEFT)

        self.files_frm = tk.Frame(self.frame1)
        self.files_frm.grid(row=3, column=0)
        
        self.added_files_frm = tk.Frame(self.files_frm)
        self.added_files_frm.pack(pady=20, side=tk.LEFT)
        self.added_files_label = tk.Label(self.added_files_frm, text="Media Files Added")
        self.added_files_label.pack()
        self.listbox_added = tk.Listbox(self.added_files_frm, width=50)
        self.listbox_added.pack(pady=10, side=tk.LEFT, fill=tk.BOTH)
        self.list_added_scroll = tk.Scrollbar(self.added_files_frm)
        self.list_added_scroll.pack(side=tk.RIGHT, fill=tk.BOTH) 
        self.listbox_added.config(yscrollcommand=self.list_added_scroll.set) 
        self.list_added_scroll.config(command=self.listbox_added.yview) 

        self.send_remove_frm = tk.Frame(self.files_frm)
        self.send_remove_frm.pack(side=tk.LEFT)
        self.send_button = tk.Button(self.send_remove_frm, text="Send File to Server", command=self.send_file)
        self.send_button.pack(pady=10)
        self.delete_button = tk.Button(self.send_remove_frm, text="Remove from server", command=self.delete_file)
        self.delete_button.pack(pady=10)
        # self.add_button = tk.Button(self.root, text="Add File", command=self.add_file)
        # self.add_button.pack(pady=10)

        self.cloud_files_frm = tk.Frame(self.files_frm)
        self.cloud_files_frm.pack(pady=20, side=tk.LEFT)
        self.cloud_files_label = tk.Label(self.cloud_files_frm, text="Media Files Uploaded")
        self.cloud_files_label.pack()
        self.listbox_cloud = tk.Listbox(self.cloud_files_frm, width=50)
        self.listbox_cloud.pack(pady=10, side=tk.LEFT, fill=tk.BOTH)
        self.list_cloud_scroll = tk.Scrollbar(self.cloud_files_frm)
        self.list_cloud_scroll.pack(side=tk.RIGHT, fill=tk.BOTH) 
        self.listbox_cloud.config(yscrollcommand=self.list_cloud_scroll.set) 
        self.list_cloud_scroll.config(command=self.listbox_cloud.yview)

    def browse_files(self):
        filetype = (('video files', '*.mp4'),
                 ('image files', '*.png *.jpeg *.jpg'),
                 ('all files', '*.*')
                )
        file_path = fd.askopenfilenames(title="Select File(s)",
                                       filetypes=filetype)
        # Change label contents
        if file_path:
            if self.local_file.add_file(file_path): # True if file_path appended to local_file 
                self.listbox_added.insert(tk.END, file_path)
                self.instructions.configure(text="File(s) added to the list. ", fg="darkviolet") # for multi file selection
            else:
                messagebox.showerror("Error", "No files selected or file not found!")
        # Below lines used when a Entry box needed
        # self.entry.delete(0, tk.END)
        # self.entry.insert(tk.END, filename)

    def remove_file(self):
        # Remove from local storage
        selection = self.listbox_added.curselection()
        if selection:
            index = selection[0]
            self.listbox_added.delete(index) # Delete from listbox
            self.local_file.delete_file(index) # Delete from storage
            self.instructions.configure(text="File removed from the storage. ",fg="darkviolet")
        else:
            messagebox.showwarning("Warning", "Please select a file to remove!")
        
    # Select file from added list and send to server
    def send_file(self):
        selection = self.listbox_added.curselection()
        if selection:
            index = selection[0]
            file_path = self.local_file.get_files()[index]
            
            if self.cloud_file.add_file(file_path): # True if file_path appended to cloud_file 
                # self.send_to_device(file_path)
                self.listbox_cloud.insert(tk.END, file_path)
                # update playback list
                file_name, file_type = self.get_filename_ext(file_path, index) # shortened to filename.ext
                self.pb_list.insert(tk.END, f" {file_name}.{file_type}")
                self.instructions.configure(text="File sent to the device. ",fg="darkviolet")
            else:
                messagebox.showwarning("Warning", "File did not send!")
        else:
            messagebox.showwarning("Warning", "Please select a file to send!")

    def send_to_device(file_path):
        try:
            if file_path:
                with open(file_path, "rb") as file:
                    #socket
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    host_ip = '10.13.26.224' # localhost
                    port = 9999

                    client_socket.connect((host_ip, port))

                    data = file.read()
                    data_serialized = pickle.dumps(data)

                    client_socket.sendall(struct.pack("Q", len(data_serialized)))
                    client_socket.sendall(data_serialized)

                    print("File sent successfully")

                    client_socket.close()
        except Exception as e:
            print("Error sending file", e)

    # Add: move selected files from right listbox to left listbox
    def delete_file(self):
        # Remove from cloud storage
        selection = self.listbox_cloud.curselection()
        if selection:
            index = selection[0]
            # file_path = self.cloud_file.get_files()[index] 
            self.listbox_cloud.delete(index) # delete from cloud listbox
            self.cloud_file.delete_file(index) # delete from cloud
            self.pb_list.delete(index) # add to listbox_added
            self.instructions.configure(text="File removed from device. ", fg="darkviolet")
        else:
            messagebox.showwarning("Warning", "Please select a file to remove from uploads!")
        
    def playback_ui(self):
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(pady=20, padx=20, side=tk.LEFT)

        self.playback_title = tk.Label(self.frame2, text="Double-click to play.\n Click on PAUSE to pause the media. ")
        self.playback_title.grid(row=0, column=0)

        self.pb_list_frm = tk.Frame(self.frame2)
        self.pb_list_frm.grid(row=1, column=0)
        # Listbox properties
        self.list_font = tk.font.Font(family="Laksaman")
        # style = ttk.Style()
        # # self.style.theme_use('classic')
        # style.configure("Vertical.TScrollbar", troughcolor="white", background="green", bordercolor="red", arrowcolor="white")

        #Adding transparent background property
        
        self.pb_list = tk.Listbox(self.pb_list_frm, 
                                  borderwidth=0, 
                                  highlightthickness=0, # remove listbox border
                                  relief=tk.FLAT, # Default: SUNKEN
                                  font=self.list_font, 
                                  fg="darkviolet", # Font color
                                  cursor="hand2") 
        self.pb_list.bind('<Double-Button-1>') # double-click add command
        # self.pb_list.attributes('-alpha',0.5)
        self.pb_list.pack(side=tk.LEFT)
        self.pb_scroll = ttk.Scrollbar(self.pb_list_frm, style="Vertical.TScrollbar") # Define scrollbar
        self.pb_scroll.pack(side=tk.RIGHT, fill=tk.BOTH) 
        self.pb_list.config(yscrollcommand=self.pb_scroll.set)  # Link scrollbar with listbox
        self.pb_scroll.config(command=self.pb_list.yview) # Scrollability

        self.pb_btn_frm = tk.Frame(self.frame2)
        self.pb_btn_frm.grid(row=2, column=0, sticky="e")
        self.pause_btn = tk.Button(self.pb_btn_frm, text="PAUSE", cursor="hand2")
        self.pause_btn.pack(pady=10, side=tk.RIGHT)

    def get_filename_ext(self, file_path, index):
        # Extract file names and extensions from paths
        file_name = os.path.basename(file_path)
        file_name, file_type = os.path.splitext(file_name)
        return file_name, file_type

    # def pause_vid(self):
        

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


# # Frame 3--control panel
# ctrl_frm = tk.Frame(root, height=100)
# ctrl_label = tk.Label(ctrl_frm, text="Control center", font=20).pack(padx=20, pady=10)
# L_light = tk.Button(ctrl_frm, text="Left light").pack(side=tk.LEFT, padx=20, pady=20)
# C_light = tk.Button(ctrl_frm, text="Center light").pack(side=tk.LEFT, padx=20, pady=20)
# R_light = tk.Button(ctrl_frm, text="Right light").pack(side=tk.LEFT, padx=20, pady=20)
# ctrl_frm.pack(side=tk.LEFT,expand=True)

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
