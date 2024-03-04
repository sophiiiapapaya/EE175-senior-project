import socket
import tkinter as tk
import end_device_client

def create_socket(end_device_ip):
    global client_socket
    # self.end_device_hostname = end_device_client.end_device_hostname()
    
    # # Create an entry widget for entering the end device's IP address
    # label_hostname = tk.Label(window, text="End Device hostname:")
    # label_hostname.pack()
    # entry_hostname = tk.Entry(window)
    # entry_hostname.pack()
    # entry_hostname.insert(0, self.end_device_hostname)
    
    #     # Create a button
    # button = tk.Button(window, text="Connect to End Device", command=self.on_button_click)
    # button.pack(pady=10)
        
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        # Specify the end device's port
        end_device_port = 12345
            
        # Connect to the end device
        client_socket.connect((end_device_ip, end_device_port))

        # message = input("Enter message to send to server: ")
        
        # message_to_end_device("GUI Client received message")

    except Exception as e:
        print("Error:", e)
    
def on_button_click():
    global end_device_hostname
    # This function will be called when the button is clicked
    message = "Message from GUI client"
    # end_device_hostname = entry_hostname.get() # Get the hostname from the entry widget
    end_device_ip = get_ip_address(end_device_hostname) 
    print(f"The IP address of {end_device_hostname} is {end_device_ip}")
    message_to_end_device(message)
    
def get_ip_address(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return "Unable to resolve IP address."

# send media
# send_media_cv2.py
def media_to_end_device(media):
    global client_socket
    try:
        # Send message to the end device
        client_socket.sendall(media.encode('utf-8'))
            
        # Receive response from the end device (if needed)
        response = client_socket.recv(1024).decode('utf-8')
        print("Response from end device:", response) # make it a window playing on operator side
            
        # Close the connection
        client_socket.close()
    except Exception as e:
        print("Error:", e)
    
# send message 
def message_to_end_device(message):
    try:
        # Send message to the end device
        client_socket.sendall(message.encode('utf-8'))
    
            
        # Receive response from the end device (if needed)
        response = client_socket.recv(1024).decode('utf-8')
        print("Response from end device:", response)
            
        # Close the connection
        client_socket.close()
    except Exception as e:
        print("Error:", e)

# def create_gui():
#     # Create GUI window
#     window = tk.Tk()
#     window.title("GUI Client")

#     # hostname = "example.com"  # Replace with the hostname you want to look up
#     # ip_address = get_ip_address(hostname)
    
#     # # Create an entry widget for entering the end device's IP address
#     # label_ip = tk.Label(window, text="End Device IP:")
#     # label_ip.pack()
#     # entry_ip = tk.Entry(window)
#     # entry_ip.pack()
#     app = GUI_Client(window)
#     # Run the GUI
#     window.mainloop()

if __name__ == "__main__":
    # create_gui()
    create_socket()

