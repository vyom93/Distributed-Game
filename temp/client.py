import tkinter as tk
import socket

class LoginWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Login")
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self.master, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.password_label = tk.Label(self.master, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack()

        self.signup_button = tk.Button(self.master, text="Signup", command=self.signup)
        self.signup_button.pack()

        self.status_label = tk.Label(self.master, text="")
        self.status_label.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Set up the client
        HOST = "127.0.0.1"
        PORT = 65431

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # Send login request to server
            s.sendall(f"login {username} {password}".encode())

            # Receive response from server
            data = s.recv(1024)
            self.status_label.config(text=data.decode())

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Set up the client
        HOST = "127.0.0.1"
        PORT = 65431

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # Send signup request to server
            s.sendall(f"signup {username} {password}".encode())

            # Receive response from server
            data = s.recv(1024)
            self.status_label.config(text=data.decode())

root = tk.Tk()
login_window = LoginWindow(root)
login_window.pack()
root.mainloop()
