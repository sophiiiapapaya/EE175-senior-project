import tkinter as tk
from tkinter import filedialog

# create tkinter for --
#  1. upload files/folder and playback in order
#  2. change order?
#  3. control panel with functional buttons (area light, select and play)
#  4. Select device

# create window
window = tk.Tk()
window.title('Smart mirror')

# Frame 1--container of widgets
upload_frm = tk.Frame(
    window, 
    width=180, 
    height=100, 
    highlightthickness=2, 
    highlightbackground="black"
)


# create upload widget
# Function for opening the 
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)

label_file_explorer = tk.Label(upload_frm, text="Click the button below to upload files").pack(padx=20, pady=10)
upload_btn = tk.Button(upload_frm, text="Browse Files").pack(padx=20, pady=25)
add_file = tk.Button(upload_frm, text="Add file", command=browseFiles).pack(padx=20, pady=20)
upload_frm.pack(side=tk.TOP, expand=True, padx=20, pady=20)

# Frame--select device
device_frm = tk.Frame(window, width=180, height=100)
# device_frm.columnconfigure(0, minsize=250)
# device_frm.rowconfigure([0, 1], minsize=100)
device_frm.pack()
select_label = tk.Label(device_frm, text="Choose the device to control", font=20).grid(row=0, column=0, sticky="w")
device1 = tk.Button(device_frm, text="device name 1").grid(row=1, column=0) # Receive device names from the same network
device2 = tk.Button(device_frm, text="device name 2").grid(row=2, column=0) # Receive device names from the same network


# Frame 2--change playback order
order_frm = tk.Frame(master=window) 
order_label = tk.Label(order_frm, text="Media added", font=20).pack(padx=20, pady=10)
order_des = tk.Label(order_frm, text="Click to instant play or move items to change the order").pack()
list_frm = tk.Frame(order_frm)
title1 = tk.Button(list_frm, relief=tk.FLAT, text="1. Video 1.{media_type}", fg="blue")
length_1 = tk.Label(list_frm, text="03:10").pack(side=tk.RIGHT)
title1.pack(pady=10)
list_frm.pack(side=tk.LEFT)

order_frm.pack(fill=tk.Y, side=tk.RIGHT, expand=True)

# Frame 3--control panel
ctrl_frm = tk.Frame(window, height=100)
ctrl_label = tk.Label(ctrl_frm, text="Control center", font=20).pack(padx=20, pady=10)
L_light = tk.Button(ctrl_frm, text="Left light").pack(side=tk.LEFT, padx=20, pady=20)
C_light = tk.Button(ctrl_frm, text="Center light").pack(side=tk.LEFT, padx=20, pady=20)
R_light = tk.Button(ctrl_frm, text="Right light").pack(side=tk.LEFT, padx=20, pady=20)
ctrl_frm.pack(side=tk.LEFT,expand=True)

# Start the application
window.mainloop() # listens for event (loop)

