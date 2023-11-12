import socket
import threading
import sys
import traceback

threads = []
nickname = None
most_recent_message = None

class Client:
    nickname = None
    client = None
    
    def __init__(self, client, nickname):
        self.nickname = nickname
        self.client = client
        
def receive_from_server():
    while True:
        try:
            message = client.recv(1024).decode("ascii") # client's first message has to be a nickname
            if message == "NICK":   
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except Exception:
            print(traceback.format_exc())
            client.close()
            break
        
def post():
    while True:
        message = input("Send a message: ")
        client.send(f"\n{nickname}: {message}".encode("ascii"))
    
if __name__ == "__main__":
    nickname = input("Create a nickname: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 42069)) # connect to server IP address
    try:
        receive_thread = threading.Thread(target=receive_from_server)
        threads.append(receive_thread)
        receive_thread.start()
        posting_thread = threading.Thread(target=post)
        threads.append(posting_thread)
        posting_thread.start()
    except (Exception, KeyboardInterrupt) as e:
        client.close()
        for t in threads:
            t.kill_received = True
        sys.exit(e)
        