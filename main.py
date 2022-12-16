import ssl
import socket
import threading
import time

usernames = open("usernames.txt").read().splitlines()

handles = []


class Solo:
    def __init__(self, username):
        self.username = str(username)
        self.encoded = self.username.encode()
        self.flag = b"HTTP/1.1 404"
        self.claimableFlag = ""
        self.claimable = None
        self.rr = 276
        self.file = open("results.txt", "a")
        
    def validate(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.create_default_context().wrap_socket(s, server_hostname="api.solo.to")
        ssl_sock.connect(("api.solo.to", 443))
        ssl_sock.send(
        b"GET /"
        + self.encoded
        + b" HTTP/1.1\r\nHost: api.solo.to\r\nConnection: close\r\nUser-Agent: x\r\n\r\n")
        data = ssl_sock.recv(self.rr)
        if b"429" in data:
            print("Ratelimited on %s, retrying..."% self.username)
            time.sleep(10)
            Solo(self.username).validate()
            
        if self.flag in data:
            print ("Found a valid username: %s" %self.username)
            self.file.write(f"\n{self.username}")
        else:
            print("Invalid username: %a" %self.username)
            
            
for i in usernames:
    handles.append(Solo(i))

for handle in handles:
    threading.Thread(target=handle.validate).start()
