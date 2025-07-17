import socket
import threading
import os

HOST = '0.0.0.0'
PORT = PORT = int(os.getenv("PORT", "64000")

clients = {}

def handle_client(conn, addr):
    player_id = addr[1]  # Use port as simple ID
    clients[player_id] = conn
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            broadcast(f"{player_id}:{data}", sender_id=player_id)
    except:
        pass
    finally:
        print(f"[DISCONNECT] {addr}")
        conn.close()
        del clients[player_id]
        broadcast(f"{player_id}:DISCONNECT", sender_id=player_id)

def broadcast(message, sender_id):
    for pid, client in clients.items():
        if pid != sender_id:
            try:
                client.send(message.encode())
            except:
                pass

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is running on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

start()
