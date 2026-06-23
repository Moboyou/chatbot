import socket
import threading
#private [name] [message] برای ارسال پیام خصوصی فرمت به این صورت باشد
#ییام عمومی را به صورت ساده و بدون عنوان publicارسال کنید.
#Bye. ییام برای خروج کاربر
HOST = '127.0.0.1'
PORT = 15000

clients = {}#adress
usernames = {}#name


def broadcast(message, sender=None):
    for client in clients.keys():
        print(clients,type(client))
        if usernames[client] != sender:
            client.send(message)


def handle_client(client_socket, addr):
    print(f"Connection from {addr} has been established.")

    # دریافت نام کاربری
    username = client_socket.recv(1024).decode('utf-8')
    if username in usernames.values():
        client_socket.send("Username already taken. Please try again.".encode('utf-8'))
        client_socket.close()
        return

    clients[client_socket] = addr
    usernames[client_socket] = username

    welcome_message = f"Hi {username}!  welcome to the chat room."
    client_socket.send(welcome_message.encode('utf-8'))
    n=f"{username} has joined the chat.".encode('utf-8')
    print(type(n))
    broadcast(f"{username} has joined the chat.".encode('utf-8'),username)

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"{username}: {message.decode('utf-8')}")
                if message.decode('utf-8').startswith("private "):
                    _, recipient, msg = message.decode('utf-8').split(" ", 2)
                    if recipient in usernames.values():
                        recipient_socket = list(clients.keys())[list(usernames.values()).index(recipient)]
                        recipient_socket.send(f"Private from {username}: {msg}".encode('utf-8'))
                    else:
                        client_socket.send("User not found.".encode('utf-8'))
                elif message.decode('utf-8')=="Please send the list of attendees.":#گرفتن لیست اعضا
                    attendee_list = ", ".join(usernames.values())
                    client_socket.send(f"Attendees are: {attendee_list}".encode('utf-8'))
                elif message.decode('utf-8')=="Bye.":# خروج کاربر
                    break
                else:
                    broadcast(f"{username}: {message.decode('utf-8')}".encode('utf-8'),username)
            else:
                break
        except:
            break
    #تا وقتی که شخص پیامی را ارسال کند این حلقه کار میکند مگر در موارد bye و بستن ترمینال
    print(f"{username} has disconnected.")
    broadcast(f"{username} has left the chat.".encode('utf-8'),username)
    del clients[client_socket]
    del usernames[client_socket]
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()


start_server()
