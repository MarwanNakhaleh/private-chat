import threading
import socket
import time
import sys
import traceback

from client import Client

threads = []

host = "127.0.0.1"
port = 42069

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # internet socket on TCP
server.bind((host, port))
server.listen()

users = []

def broadcast(message: str):
    try:
        message = message.encode("ascii")
    except AttributeError: # message already encoded
        pass 
    for user in users:
        user.client.send(message)

def handle(client, nickname):
    while True:
        time.sleep(1)
        try:
            message = client.recv(1024)
            broadcast(message)
        except Exception as e:
            print("unable to broadcast the message: " + traceback.format_exc())
            try:
                failed_user = [user for user in users if user.nickname == nickname]
                users.remove(failed_user)
            except ValueError: # user not in list of users
                print("user not in user list")
            client.close() # change this to close the client's ip
            broadcast(f"{client.nickname} left the chat")
            
def receive():
    while True:
        client, address = server.accept()
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode("ascii")
        new_client = Client(client, nickname) # message is nickname
        users.append(new_client)
        print(f"{new_client.nickname} connected from IP address {str(address)}\n")
        broadcast(f"\n{new_client.nickname} entered the chat")
        
        thread = threading.Thread(target=handle, args=(client, new_client.nickname,))
        threads.append(thread)
        thread.start()
        
if __name__ == "__main__":
    print(f"starting server at address {socket.gethostbyname(socket.gethostname())}")
    try:
        receive()
    except (Exception, KeyboardInterrupt) as e:
        print(traceback.format_exc())
        server.close()
        for t in threads:
            t.kill_received = True
        sys.exit(e)
        