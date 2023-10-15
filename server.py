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
connections = []


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
                print(f"[{addr}]{username}: disconnected")
                conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
                
                messages.append((addr, '[DECONNECTION]'))
            
            elif msg.startswith('username: '):
                username = msg[10:]
                print(f"[{addr}] username is now {username}")
                for connection in connections:
                    if connection[1] == addr:
                        if len(connection) == 2:
                            connection.append(username)
                        else:
                            connection[2] = username
            
            else:
                print(f"[{addr}]{username}: {msg}")
                messages.append((addr, msg))
    
    if username != "":
        connections.remove([conn, addr, username])
    else:
        connections.remove([conn, addr])
    conn.close()

def handle_messages():
    while True:
        new_messages = messages.copy()
        if new_messages != []:
            for message in new_messages:
                for conn in connections:
                    if message[0] != conn[1]:
                        username = conn[-1]
                        conn[0].send(f"{username}: {message[1]}".encode(FORMAT))
                messages.remove(message)


message_thread = threading.Thread(target=handle_messages)


def start():
    server.listen()
    print(f"[LISTENING] server is listening on {ADDR}")
    message_thread.start()
    while True:
        conn, addr = server.accept()
        connections.append([conn, addr])
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")


print('[STARTING] serveris starting...')
start()






