import socket
import threading

# Server configuration
HOST = '0.0.0.0'   # Listen on all network interfaces
PORT = 8003

# Lists to keep track of clients and nicknames
clients = []
nicknames = []

# Broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            remove_client(client)

# Remove a client safely
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast(f"Server: {nickname} left the chat.".encode('utf-8'))

# Handle messages from a specific client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message)
        except:
            break

    remove_client(client)

# Accept incoming connections
def receive_connections():
    print(f"Server running on port {PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        # Receive nickname
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Notify client
        client.send("Server: Connected to the chat room.".encode('utf-8'))
        broadcast(f"Server: {nickname} joined the chat.".encode('utf-8'))

        # Start client thread
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

receive_connections()