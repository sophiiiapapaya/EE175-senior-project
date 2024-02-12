import tkinter as tk

# create tkinter for --
#  1. upload files/folder and playback in order
#  2. change order?
#  3. control panel with functional buttons (area light, select and play)

# create window
window = tk.Tk()

# Frame--container of widgets
upload_frm = tk.Frame()

# create upload widget
upload_ln = tk.Label(master=upload_frm, text="Click the button below to upload files/folder")
upload_ln.pack() # add widget to the window

upload_btn = tk.Button(master=upload_frm, text="Click to upload")
upload_btn.pack()

upload_frm.pack(fill=tk.BOTH, expand=True)

# Frame--change playback order
order_frm = tk.Frame()

# Create order widget
order_des = tk.Label(master=order_frm, text="Media play in the order shown. Move items to change the order")

# Start the application
window.mainloop() # listens for event (loop)

