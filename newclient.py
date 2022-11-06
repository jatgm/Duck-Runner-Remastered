import socket
import threading

class Client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self):
        self.sock.connect((socket.gethostbyname(socket.gethostname()), 8080))
        self.sock.send(bytes('Belly', 'utf-8')) #name
        self.start = False
        self.first = False
        self.player_two_jump = True
        self.spawn = ""
        self.connected = False

        recieveThread = threading.Thread(target=self.recieveMessage)
        recieveThread.daemon = True
        recieveThread.start()

    def sendMsg(self,msg):
        self.sock.send(bytes(msg, 'utf-8')) #name

    def recieveMessage(self):
        while True:
            data = str(self.sock.recv(1024), 'utf-8')
            if not data:
                break
            try:
                self.spawn = int(data)
            except ValueError:                
                if data == "start":
                    self.start = True
                if data == "disconnect":
                    self.start = False
                    self.first = True
                if data == "first":
                    self.first = True
                if data == "jump":
                    self.player_two_jump = True
            self.connected = True
            print(data)
    