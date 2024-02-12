import tkinter as tk

# create tkinter for --
#  1. upload files/folder and playback in order
#  2. change order?
#  3. control panel with functional buttons (area light, select and play)

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
upload_ln = tk.Label(upload_frm, text="Click the button below to upload files/folder").pack(padx=20, pady=10) # add widget to the window
upload_btn = tk.Button(upload_frm, text="Click to upload").pack(padx=20, pady=25)
add_file = tk.Button(upload_frm, text="Add file").pack(padx=20, pady=20)
upload_frm.pack(side=tk.TOP, expand=True, padx=20, pady=20)

# Frame 3--change playback order
order_frm = tk.Frame(master=window) 
order_label = tk.Label(order_frm, text="Media added", font=20).pack(padx=20, pady=10)
order_des = tk.Label(order_frm, text="Click to instant play or move items to change the order").pack()
list_frm = tk.Frame(order_frm)
title1 = tk.Button(list_frm, relief=tk.FLAT, text="1. Video 1.{media_type}", fg="blue")
length_1 = tk.Label(list_frm, text="03:10").pack(side=tk.RIGHT)
title1.pack(pady=10)
list_frm.pack(side=tk.LEFT)

order_frm.pack(fill=tk.Y, side=tk.RIGHT, expand=True)

# Frame 2--control panel
ctrl_frm = tk.Frame(window, height=100)
ctrl_label = tk.Label(ctrl_frm, text="Control center", font=20).pack(padx=20, pady=10)
L_light = tk.Button(ctrl_frm, text="Left light").pack(side=tk.LEFT, padx=20, pady=20)
C_light = tk.Button(ctrl_frm, text="Center light").pack(side=tk.LEFT, padx=20, pady=20)
R_light = tk.Button(ctrl_frm, text="Right light").pack(side=tk.LEFT, padx=20, pady=20)
ctrl_frm.pack(side=tk.LEFT,expand=True)


# Start the application
window.mainloop() # listens for event (loop)

