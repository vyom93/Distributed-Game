import socket
import sqlite3

# Set up the server
HOST = "127.0.0.1"
PORT = 65431

# Set up the database
conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
conn.commit()

def add_user(username, password):
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    user_id = cur.lastrowid
    return user_id

def find_user(username, password):
    cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    if result is not None:
        user_id = result[0]
        return user_id
    else:
        return None

# Set up the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            while True:
                # Receive data from client
                data = conn.recv(1024)

                # If client has disconnected, break the loop
                if not data:
                    break

                # Decode the data and split it into parts
                message = data.decode()
                parts = message.split()

                # Handle the command
                command = parts[0]

                if command == "signup":
                    username = parts[1]
                    password = parts[2]

                    user_id = add_user(username, password)
                    if user_id is not None:
                        response = f"User {username} signed up with ID {user_id}"
                    else:
                        response = "Error signing up user"

                    # Send response to client
                    conn.sendall(response.encode())

                elif command == "login":
                    username = parts[1]
                    password = parts[2]

                    user_id = find_user(username, password)
                    if user_id is not None:
                        response = f"User {username} logged in with ID {user_id}"
                    else:
                        response = "Invalid username or password"

                    # Send response to client
                    conn.sendall(response.encode())

                else:
                    response = "Invalid command"
                    conn.sendall(response.encode())
