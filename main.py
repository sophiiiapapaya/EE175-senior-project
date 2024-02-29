# main.py
import server
import gui_client
import end_device_client
import tkinter as tk
from gui import GUI

def main():
    # Call gui
    root = tk.Tk() 
    root.title("Smart Mirror") 
    app = GUI(root) 
    root.mainloop() # Start the application. listens for event (loop)
    
    # Call server
    server.run_server()

    # Call GUI client
    gui_client.run_gui_client()

    # Call end device client
    end_device_client.run_end_device_client()

if __name__ == "__main__":
    main()
