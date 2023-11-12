import socket
import threading
import sys, os
import traceback

visible_messages = []
nickname = None
most_recent_message = None
exception_happened = False

class Client:
    nickname = None
    client = None
    
    def __init__(self, client, nickname):
        self.nickname = nickname
        self.client = client
        
def print_messages(new_message):
    os.system('cls' if os.name == 'nt' else 'clear')
    visible_messages.append(new_message)
    for msg in visible_messages:
        print(msg)

def receive_from_server():
    while True:
        try:
            message = client.recv(1024).decode("ascii") # client's first message has to be a nickname
            if message == "NICK":   
                client.send(nickname.encode("ascii"))
            elif not message.startswith(nickname):
                print_messages(message)
        except Exception:
            print(traceback.format_exc())
            client.close()
            break
        
def post():
    while True:
        message = input("")
        print_messages(f"Me: {message}")
        client.send(f"{nickname}: {message}".encode("ascii"))
        
if __name__ == "__main__":
    nickname = input("Create a nickname: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 42069)) # connect to server IP address
    try:
        posting_thread = threading.Thread(target=post)
        posting_thread.start()
        receive_thread = threading.Thread(target=receive_from_server)
        receive_thread.start()
    except KeyboardInterrupt:
        print("Exiting now, thanks for chatting!")
        exception_happened = True
    except ConnectionResetError:
        print("Connection ended by server!")
        exception_happened = True
    except Exception as e:
        print("There was an error in the program!")
        print(traceback.format_exc())
        exception_happened = True
    if exception_happened:
        client.send(f"\n{nickname} left the chat") 
        client.close()
        sys.exit(0)
        