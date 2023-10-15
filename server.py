import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

messages = []


def handle_client(conn: socket.socket, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    
    username = ""
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:   # si le message est pas celui de premiere connection (c'est un message vide)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg.startswith('username: '):
                username = msg[10:]
            else:
                print(f"[{addr}]{username}: {msg}")
                messages.append((addr, msg))
    
    
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print('[STARTING] serveris starting...')
start()






