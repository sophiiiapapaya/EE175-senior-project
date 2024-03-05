import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox, font, ttk
import customtkinter
from PIL import Image, ImageTk
import os
import end_device_client# import gui_client.py and end_device_client.py
import cv2, pickle, struct, socket

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
        self.root = master
        self.root.title("Smart Mirror Control Station")
        self.local_file = Local_File()
        self.cloud_file = Cloud_File()
        # self.server_socket = server.Server_Socket()
        # self.server_socket.connect_client()
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #-------------------variables---------------------------
        self.playing = False # initial state: all paused
        self.start_stream = False 
        self.img_path_list = ['assets/start-img.png', 'assets/stream-img.png', 'assets/stop-img.png']
        self.img_list = []
        self.pb_buttons = []
        self.light_btns = []
        self.load_images()

        #-------------------styles-------------------------------
        self.label_font = font.Font(slant="italic")
        self.color = {
            "rose" : "#C77C78",
            "blue" : "#59BACC",
            "green" : "#58AD69", 
            "orange" : "#FFBC49",
            "red" : "#E2574C", 
            "light-gray": "#b5b5b5"
        }
        
        #-------------------call ui-------------------------------
        self.section1 = tk.Frame(self.root)
        self.section1.pack(side=tk.LEFT, expand=True)
        self.status = tk.Label(self.section1, text="<Nothing playing>", fg="darkviolet", wraplength=245, justify=tk.LEFT)
        self.status.pack(padx=20, side=tk.TOP, anchor="n")
        
        self.select_device_ui()
        self.playback_ui()
        self.manage_file_ui()
        self.control_ui()

        #------------------build connection-----------------------
    
        self.client_socket.connect((self.ip_address, 12345))
    
    def load_images(self):
        for path in self.img_path_list:
            btn_image = ImageTk.PhotoImage(Image.open(path).resize((20, 20), Image.LANCZOS))
            self.img_list.append(btn_image)
        self.pause_img = ImageTk.PhotoImage(Image.open('assets/pause-img.png').resize((20, 20), Image.LANCZOS))
        
    def playback_ui(self):
        
        self.frame1 = tk.Frame(self.section1)
        self.frame1.pack(pady=20, padx=20, side=tk.TOP, expand=True)


        self.playback_title = tk.Label(self.frame1, text="Select file and click an action button.")
        self.playback_title.pack(padx=20, side=tk.TOP, anchor='nw')
        
        # Key descriptions
        keys_list = """Keyboard:\n \'p\' to pause\n \'q\' to end\n Any key to resume video"""
        self.keys_usage = tk.Label(self.frame1, text=keys_list, justify=tk.LEFT)
        self.keys_usage.pack(padx=20, side=tk.TOP, anchor='nw')

        self.pb_list_frm = tk.Frame(self.frame1)
        self.pb_list_frm.pack(padx=20, side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Listbox properties
        self.pb_list = tk.Listbox(self.pb_list_frm, 
                                  borderwidth=0, 
                                  highlightthickness=0, # remove listbox border
                                  relief=tk.FLAT, # Default: SUNKEN
                                  selectbackground="darkviolet",
                                  cursor="hand2") 
        self.pb_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pb_list.bind('<<ListboxSelect>>',self.pb_action)
        self.pb_scroll = ttk.Scrollbar(self.pb_list_frm, style="Vertical.TScrollbar") # Define scrollbar
        self.pb_scroll.pack(side=tk.RIGHT, fill=tk.Y) 
        self.pb_list.config(yscrollcommand=self.pb_scroll.set)  # Link scrollbar with listbox
        self.pb_scroll.config(command=self.pb_list.yview) # Scrollability
        
        self.btn_frm = tk.Frame(self.frame1)
        self.btn_frm.pack(padx=10, side=tk.TOP, anchor='nw', fill=tk.NONE)

        self.btn_cmds =[self.restart_cmd, self.stream_cmd, self.stop_cmd]
        
        self.start_img = ImageTk.PhotoImage(Image.open('assets/start-img.png').resize((20, 20), Image.LANCZOS))
        restart_btn = tk.Button(self.btn_frm,
                               image=self.start_img, 
                               text="Restart",
                               cursor="hand2", 
                               command=self.restart_cmd)
        restart_btn.pack(pady=10, padx=10, side=tk.LEFT)
        
        self.stop_img = ImageTk.PhotoImage(Image.open('assets/stop-img.png').resize((20, 20), Image.LANCZOS))
        stop_btn = tk.Button(self.btn_frm,
                               image=self.stop_img, 
                               text="Stop",
                               cursor="hand2", 
                               command=self.stop_cmd)
        stop_btn.pack(pady=10, padx=10, side=tk.LEFT)

    def select_device_ui(self):
        self.frame3 = tk.Frame(self.section1)
        self.frame3.pack(pady=20, padx=20, side=tk.TOP, expand=True)

        self.select_device_title = tk.Label(self.frame3, text="Choose your device and click connect.")
        self.select_device_title.pack(padx=20, side=tk.TOP, anchor='nw')

        self.device_list_frm = tk.Frame(self.frame3)
        self.device_list_frm.pack(padx=20, side=tk.TOP, fill=tk.BOTH, expand=True)

        # Listbox properties
        self.device_list = tk.Listbox(self.device_list_frm, 
                                  borderwidth=0, 
                                  highlightthickness=0, # remove listbox border
                                  relief=tk.FLAT, # Default: SUNKEN
                                  selectbackground="darkviolet",
                                  cursor="hand2") 
        self.device_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.device_list.bind('<<ListboxSelect>>',self.connect_device)
        # self.device_list.insert(tk.END, self.end_device_hostname)

        self.device_list_scroll = ttk.Scrollbar(self.device_list_frm, style="Vertical.TScrollbar") # Define scrollbar
        self.device_list_scroll.pack(side=tk.RIGHT, fill=tk.Y) 
        self.device_list.config(yscrollcommand=self.device_list_scroll.set)  # Link scrollbar with listbox
        self.device_list_scroll.config(command=self.device_list.yview) # Scrollability
        self.hostname, self.ip_address = end_device_client.get_hostname_ip()
        self.device_list.insert(tk.END, f"{self.ip_address}: {self.hostname}")

        self.conn_device_btn = customtkinter.CTkButton(self.frame3, 
                                                        text="Connect", 
                                                        cursor="hand2", 
                                                        command=self.connect_cmd,
                                                        text_color="#000000", 
                                                        fg_color="transparent", 
                                                        hover_color=self.color["orange"], 
                                                        border_width=1)
        self.conn_device_btn.pack(pady=10, padx=10, side=tk.TOP)

    def manage_file_ui(self):
        self.section2 = tk.Frame(self.root)
        self.section2.pack(side=tk.LEFT, expand=True)
        self.frame2 = tk.Frame(self.section2)
        # self.frame1.grid(row=0, column=0,pady=20, padx=20, sticky='nswe')
        self.frame2.pack(pady=20, padx=20, side=tk.TOP, expand=True, anchor="nw")

        self.frame5 = tk.Frame(self.frame2)
        self.frame5.pack(pady=20, side=tk.TOP, fill=tk.BOTH)
        self.title_font = tk.font.Font(size=20)
        self.manage_title = tk.Label(self.frame5, text="UPLOAD YOU FILES", font=self.title_font)
        self.manage_title.pack(side=tk.LEFT, anchor="nw")
        self.device_status = tk.Label(self.frame5, fg="darkviolet", justify=tk.LEFT)
        self.device_status.pack(anchor="ne")
        
        self.instructions = tk.Label(self.frame2, text="Click the button below to upload files")
        self.instructions.pack(padx=20, side=tk.TOP, anchor="nw")

        # self.entry = tk.Entry(self.frame, width=50)
        # self.entry.pack(side=tk.LEFT)

        self.action_frm = tk.Frame(self.frame2)
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

        self.files_frm = tk.Frame(self.frame2)
        self.files_frm.pack(padx=20, side=tk.TOP, expand=True)
        
        self.added_files_frm = tk.Frame(self.files_frm, borderwidth=1)
        self.added_files_frm.pack(side=tk.LEFT, expand=True)
        self.added_files_label1 = tk.Label(self.added_files_frm, text="Selected files will be added here. ")
        self.added_files_label1.pack()
        self.listbox_added = tk.Listbox(self.added_files_frm, borderwidth=0, width=50, height=20, selectmode = "multiple")
        self.listbox_added.pack(pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_added_scroll = ttk.Scrollbar(self.added_files_frm, style="Vertical.TScrollbar")
        self.list_added_scroll.pack(pady=10,side=tk.RIGHT, fill=tk.Y) 
        self.listbox_added.config(yscrollcommand=self.list_added_scroll.set) 
        self.list_added_scroll.config(command=self.listbox_added.yview) 
        self.file_note_frm = tk.Frame(self.frame2, borderwidth=1)
        self.file_note_frm.pack(padx=20, side=tk.TOP, fill=tk.X, expand=True)
        self.added_files_label2 = tk.Label(self.file_note_frm, text="The list is for your convenience. Highlight the files and click on > to upload", font=self.label_font)
        self.added_files_label2.pack(side=tk.LEFT, anchor='nw')
        
        self.send_remove_frm = tk.Frame(self.files_frm)
        self.send_remove_frm.pack(side=tk.LEFT)
        self.send_button = tk.Button(self.send_remove_frm, text=">", command=self.ready_to_send)
        self.send_button.pack(pady=10)
        self.delete_button = tk.Button(self.send_remove_frm, text="<", command=self.delete_file)
        self.delete_button.pack(pady=10)

        self.cloud_files_frm = tk.Frame(self.files_frm, borderwidth=1)
        self.cloud_files_frm.pack(side=tk.LEFT, expand=True)
        self.cloud_files_label = tk.Label(self.cloud_files_frm, text="Media Files Uploaded")
        self.cloud_files_label.pack()
        self.listbox_cloud = tk.Listbox(self.cloud_files_frm, borderwidth=0, width=50, height=20, selectmode = "multiple")
        self.listbox_cloud.pack(pady=10, side=tk.LEFT, expand=True)
        self.list_cloud_scroll = ttk.Scrollbar(self.cloud_files_frm, style="Vertical.TScrollbar")
        self.list_cloud_scroll.pack(pady=10,side=tk.RIGHT, fill=tk.Y) 
        self.listbox_cloud.config(yscrollcommand=self.list_cloud_scroll.set) 
        self.list_cloud_scroll.config(command=self.listbox_cloud.yview)

    def control_ui(self):
        self.frame4 = tk.Frame(self.section2)
        self.frame4.pack(pady=20, padx=20, side=tk.TOP, expand=True, anchor="nw")

        self.ctrl_title = tk.Label(self.frame4, text="CONTROL PANEL", font=self.title_font)
        self.ctrl_title.pack(pady=20, side=tk.TOP, anchor="nw")
        self.ctrl_inst = tk.Label(self.frame4, text="Click on button to enable")
        self.ctrl_inst.pack(padx=20, side=tk.TOP, anchor="nw")
        
        self.ctrl_btn_frm = tk.Frame(self.frame4)
        self.ctrl_btn_frm.pack(side=tk.TOP)

        self.light_cmds = []
        self.light_text = ["Left light", "Center light", "Right light"]
        for txt in self.light_text:
            button = customtkinter.CTkButton(self.ctrl_btn_frm, 
                                             text=txt, 
                                             cursor="hand2",  
                                             text_color="#000000", 
                                             fg_color="transparent", 
                                             hover_color=self.color["orange"], 
                                             border_width=1)
            button.pack(pady=20, padx=20, side=tk.LEFT)
            self.light_btns.append(button)

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
            self.status.configure(text="File(s) added to the list. ", fg="darkviolet") # for multi file selection
            
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
            self.status.configure(text="File removed from the storage. ",fg="darkviolet")
        else:
            messagebox.showwarning("Warning", "Please select a file to remove!")
        
    # Select file from added list and send to server
    def ready_to_send(self):
        if self.listbox_added.curselection():
            for index in self.listbox_added.curselection(): 
                file_path = self.local_file.get_files()[index]
            
                if self.cloud_file.add_file(file_path): # True if file_path appended to cloud_file 
                    self.listbox_cloud.insert(tk.END, file_path)
                    # update playback list
                    file_name, file_type = self.get_filename_ext(file_path) # shortened to filename.ext
                    self.pb_list.insert(tk.END, f"{file_name}{file_type}")
                else:
                    messagebox.showwarning("Warning", "File did not send!")
            for index in reversed(self.listbox_added.curselection()):
                # Ensure index is within valid range
                if 0 <= index < self.listbox_added.size():
                    self.listbox_added.delete(index) # Delete from listbox
                    self.local_file.delete_file(index) # Delete from storage
            self.status.configure(text="File(s) sent to the device. ",fg="darkviolet")
        else:
            messagebox.showwarning("Warning", "Please select a file to send!")


    # Add: move selected files from right listbox to left listbox
    def delete_file(self):
        # Remove from cloud storage
        if self.listbox_cloud.curselection():
            for index in self.listbox_cloud.curselection(): 
                file_path = self.cloud_file.get_files()[index]
            
                if self.local_file.add_file(file_path): # True if file_path appended to cloud_file 
                    self.listbox_added.insert(tk.END, file_path)
                else:
                    messagebox.showwarning("Warning", "File was not sent back!")
            for index in reversed(self.listbox_cloud.curselection()):
                # Ensure index is within valid range
                if 0 <= index < self.listbox_cloud.size():
                    self.listbox_cloud.delete(index)  # Delete from cloud listbox
                    self.cloud_file.delete_file(index)  # Delete from cloud_file
                    self.pb_list.delete(index)  # Delete from playback list
            self.status.configure(text="File removed from device. ", fg="darkviolet")
        else:
            messagebox.showwarning("Warning", "Please select a file to remove from uploads!")

    def get_filename_ext(self, file_path):
        # Extract file names and extensions from paths
        file_name = os.path.basename(file_path)
        file_name, file_type = os.path.splitext(file_name)
        return file_name, file_type
        
    
    # Enable buttons 
    def pb_action(self, event=None):
        selection = self.pb_list.curselection()
        if selection:
            index = selection[0]
            self.sending_path = self.cloud_file.get_files()[index]    
            file_name, file_type = self.get_filename_ext(self.sending_path)
            self.shortened_path = f"{file_name}{file_type}"
            status_txt = f"Selected \"{self.shortened_path}\". Click the button to play from where you left off or play from the beginning."
            self.status.configure(text=status_txt)

    # self.pb_buttons[1]
    def restart_cmd(self):
        
        status_txt = f"Playing \"self.shortened_path\" from the beginning"
        self.status.configure(text=status_txt)
        # restart the selected video
        self.media_to_end_device(self.sending_path) # Send the new/selected path to server
      
    # self.pb_buttons[2]
    def stream_cmd(self):
        self.status.configure(text="Connecting camera to device")
        file_path = 0 # will connect the camera
        self.media_to_end_device(file_path)

    def stop_cmd(self):
        self.client_socket.sendall("Quit".encode('utf-8'))

    def connect_device(self, event=None):
        selection = self.device_list.curselection()
        if selection:
            index = selection[0]
            device = self.device_list.get(index)            
            status_txt = f"Device selected: \"{self.hostname} ({self.ip_address})\". \nClick button to connect."
            self.device_status.configure(text=status_txt)
            # gui_client.message_to_end_device("GUI Client received message")

    def connect_cmd(self):
        self.client_socket.connect((self.ip_address, 12345))
        status_txt = f"Connected to \"{self.hostname} ({self.ip_address})\". \nClick button to connect."
        self.device_status.configure(text=status_txt)
            
    def media_to_end_device(self, file_path):
        try:        
            self.client_socket.sendall(file_path.encode('utf-8'))
            
            cap = cv2.VideoCapture(file_path)
            paused = False
            
            while cap.isOpened():
                key = cv2.waitKey(1) & 0xFF
                if not paused:
                    ret, frame = cap.read()
                    if not ret:
                        print("Video finished.")
                        break

                    cv2.imshow('Video sending', frame)
                    
                    codedFrame = pickle.dumps(frame)
                    msg = struct.pack("Q", len(codedFrame)) + codedFrame
                    try:
                        self.client_socket.sendall(msg)
                    except Exception:
                        print("Connection lost, exiting stream")
                        cap.release()
                        self.client_socket.close()
                    
                if key == ord('q'):
                    message = "Quit"
                    print(message)
                    self.client_socket.sendall(message.encode('utf-8'))
                    break
                elif key == ord('p'):
                    if paused:
                        paused = False
                        message = "Play"
                        # # Send frame to client
                        # _, buffer = cv2.imencode('.jpg', frame)
                        # data = buffer.tobytes()
                        # self.client_socket.sendall(data)
                        print(message)
                    else:
                        paused = True
                        message = "Pause"
                        print(message)
                        cv2.waitKey(-1) # wait until any key is pressed
                    self.client_socket.sendall(message.encode('utf-8'))

            # Release resources
            cap.release()
            cv2.destroyAllWindows()
            # self.client_socket.close()
        except Exception as e:
            print("Error:", e)
    
def create_gui():
    # Instantiating top level 
    root = tk.Tk() 
  
    # Setting the title of the window 
    root.title("Smart Mirror") 

    # check default font
    # print(font.nametofont('TkDefaultFont').actual())
  
    # Setting the geometry i.e Dimensions 
    # root.geometry("400x250") 
  
    # Calling our App 
    app = GUI(root) 
  
    # Mainloop which will cause this toplevel 
    # to run infinitely 
    root.mainloop() # Start the application. listens for event (loop)

if __name__ == "__main__": 
    create_gui()
