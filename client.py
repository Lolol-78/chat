import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '172.21.6.50'
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def handle_server():
    while True:
        msg = client.recv(2048).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            print('[CLIENT] disconnecting...')
            break
        print(msg)


def loop():
    while True:
        message = input()
        if message == 'disconnect':
            send(DISCONNECT_MESSAGE)
            break
        else:
            send(message)

loop_thread = threading.Thread(target=loop)
server_thread = threading.Thread(target=handle_server)

loop_thread.start()
server_thread.start()

