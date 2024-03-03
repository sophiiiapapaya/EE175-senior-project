# main.py
import time
import gui_client
import end_device_client
import tkinter as tk
# from gui import GUI

def start_gui_client():
    # Start the GUI client
    gui_client.create_gui()

def start_end_device_client():
    # Start the end device client
    end_device_client.connect_to_gui_client()
    
def main():
    
    # Start the GUI client in a separate thread
    # gui_thread = threading.Thread(target=start_gui_client)
    # gui_thread.start()
    start_gui_client()
    
    # Wait for a short duration to ensure the GUI client has started and is ready
    time.sleep(2)

    # Start the end device client
    start_end_device_client()

if __name__ == "__main__":
    main()
