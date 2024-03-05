import tkinter as tk
from tkinter import filedialog, messagebox
import os
import socket
import pickle
import struct

class FileStorage:
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

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Upload and Playback GUI")
        self.file_storage = FileStorage()

        self.setup_ui()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.entry = tk.Entry(self.frame, width=50)
        self.entry.pack(side=tk.LEFT)

        self.browse_button = tk.Button(self.frame, text="Browse Files", command=self.browse_files)
        self.browse_button.pack(side=tk.LEFT)

        self.media_frame = tk.Frame(self.root)
        self.media_frame.pack(pady=20)

        self.media_label = tk.Label(self.media_frame, text="Media Files")
        self.media_label.pack()

        self.listbox = tk.Listbox(self.media_frame, width=50)
        self.listbox.pack()

        self.add_button = tk.Button(self.root, text="Add File", command=self.add_file)
        self.add_button.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete File", command=self.delete_file)
        self.delete_button.pack(pady=10)

        self.send_button = tk.Button(self.root, text="Send File to Server", command=self.send_file)
        self.send_button.pack(pady=10)

    def browse_files(self):
        filename = filedialog.askopenfilename(title="Select File",
                                              filetypes=(("All Files", "*.*"), ("Text Files", "*.txt")))
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, filename)

    def add_file(self):
        file_path = self.entry.get()
        if file_path:
            if self.file_storage.add_file(file_path):
                self.listbox.insert(tk.END, file_path)
            else:
                messagebox.showerror("Error", "File not found!")

    def delete_file(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.listbox.delete(index)
            self.file_storage.delete_file(index)

    def send_file(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.file_storage.get_files()[index]
            self.send_to_server(file_path)
        else:
            messagebox.showwarning("Warning", "Please select a file to send!")

    def send_to_server(self, file_path):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # client_socket.connect(('192.168.1.6', 9999))
            client_socket.connect(('10.13.229.231', 9999))

            with open(file_path, 'rb') as file:
                file_data = file.read()
                file_size = len(file_data)
                message = struct.pack("Q", file_size) + file_data
                client_socket.sendall(message)

            client_socket.close()
            print(f"File {file_path} sent successfully to the server.")
        except Exception as e:
            print(f"Error occurred while sending file {file_path}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
