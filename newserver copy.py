import socket
import threading
import time
from random import randint

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = {} # This will be applied to all instances of this class (There is only one instanceXD)
    def __init__(self):
        self.sock.bind((socket.gethostbyname(socket.gethostname()), 8080))
        self.sock.listen()
        self.first = 0
    
    def disconnect(self, name, c, a):
        print(f"({name}){str(a[0])}:{str(a[1])}, disconnected")
        if self.first == c:
            self.first = 0
        del Server.connections[c]
        for connection in Server.connections: #Server.connctions not self because self would only apply to that instanc
            # connection.send(f"{name} has disconnected".encode('utf-8'))
            connection.send("disconnect".encode('utf-8'))
            self.first = connection
            
        c.close()

    def gamerun(self):
        while True:
            time.sleep(1.5)
            if len(Server.connections) > 1:
                i = randint(0,2)
                for connection in Server.connections:
                    connection.send(bytes(f"{i}", 'utf-8'))
            else:
                break

    def handler(self, c, a):
        name = str(c.recv(1024), 'utf-8') # name
        Server.connections.update({c:name})
        print(f"({name}){str(a[0])}:{str(a[1])}, connected")
        if len(Server.connections) > 1:
            spawnThread = threading.Thread(target=self.gamerun)
            spawnThread.daemon = True
            spawnThread.start()
            for connection in Server.connections:
                connection.send(bytes("start", 'utf-8'))
        else:
            for connection in Server.connections:
                self.first = c
                connection.send(bytes("first", 'utf-8'))
                
        while True:
            try:
                data = str(c.recv(1024), 'utf-8') # it will wait here
                if data:
                    for connection in Server.connections:
                        if connection != c:
                            connection.send(f"{data}".encode('utf-8'))
                else:
                    self.disconnect(name, c, a)
                    break

            except ConnectionResetError:
                self.disconnect(name, c, a)
                break

    def run(self):
        while True:
            c, a = self.sock.accept()
            connectionThread = threading.Thread(target=self.handler, args=(c, a))
            connectionThread.daemon = True
            connectionThread.start()
            print(f"{str(a[0])}:{str(a[1])}, connected")

server = Server()
server.run()