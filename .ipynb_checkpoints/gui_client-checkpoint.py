import socket
import tkinter as tk
import end_device_client

class GUI_Client:
    def __init__(self, window):
        self.root = window
        
        # global end_device_hostname
        self.end_device_hostname = end_device_client.end_device_hostname()
    
        # Create an entry widget for entering the end device's IP address
        label_hostname = tk.Label(window, text="End Device hostname:")
        label_hostname.pack()
        entry_hostname = tk.Entry(window)
        entry_hostname.pack()
        entry_hostname.insert(0, self.end_device_hostname)
    
        # Create a button
        button = tk.Button(window, text="Connect to End Device", command=self.on_button_click)
        button.pack(pady=10)
        
        try:
            # Create a socket object
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Specify the end device's port
            end_device_port = 12345
            
            # Connect to the end device
            self.client_socket.connect((self.end_device_ip, end_device_port))

        except Exception as e:
            print("Error:", e)

    # send media
    def media_to_end_device(self,message):
        try:
            # Send message to the end device
            self.client_socket.sendall(message.encode('utf-8'))
            
            # Receive response from the end device (if needed)
            response = self.client_socket.recv(1024).decode('utf-8')
            print("Response from end device:", response)
            
            # Close the connection
            self.client_socket.close()
        except Exception as e:
            print("Error:", e)
    
    # send message 
    def send_message_to_end_device(self,message):
        try:
            # Send message to the end device
            self.client_socket.sendall(message.encode('utf-8'))
            
            # Receive response from the end device (if needed)
            response = self.client_socket.recv(1024).decode('utf-8')
            print("Response from end device:", response)
            
            # Close the connection
            self.client_socket.close()
        except Exception as e:
            print("Error:", e)
    
    def on_button_click(self):
        # global end_device_hostname
        # This function will be called when the button is clicked
        message = "Message from GUI client"
        # end_device_hostname = entry_hostname.get() # Get the hostname from the entry widget
        self.end_device_ip = self.get_ip_address(self.end_device_hostname) 
        print(f"The IP address of {self.end_device_hostname} is {self.end_device_ip}")
        self.send_message_to_end_device(message)
    
    def get_ip_address(self,hostname):
        try:
            self.ip_address = socket.gethostbyname(hostname)
            return self.ip_address
        except socket.gaierror:
            return "Unable to resolve hostname."

def create_gui():
    # Create GUI window
    window = tk.Tk()
    window.title("GUI Client")

    # hostname = "example.com"  # Replace with the hostname you want to look up
    # ip_address = get_ip_address(hostname)
    
    # # Create an entry widget for entering the end device's IP address
    # label_ip = tk.Label(window, text="End Device IP:")
    # label_ip.pack()
    # entry_ip = tk.Entry(window)
    # entry_ip.pack()
    app = GUI_Client(window)
    # Run the GUI
    window.mainloop()

if __name__ == "__main__":
    create_gui()

