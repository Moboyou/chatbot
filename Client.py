import socket
import threading

HOST = '127.0.0.1'
PORT = 15000

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("An error occurred!")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input("")
        if message.lower() == "Bye.":
            client_socket.send("Bye.".encode('utf-8'))
            break
        else:
            client_socket.send(message.encode('utf-8'))
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    username = input("Enter your username: ")
    client_socket.send(username.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    send_messages(client_socket)

start_client()
