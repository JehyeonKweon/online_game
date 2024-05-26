import socket
import pickle

class Network():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '10.200.118.108'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):

        self.client.connect(self.addr)
        return self.client.recv(2048).decode()
        

    def send(self, data):

        self.client.send(str.encode(data))
        return pickle.loads(self.client.recv(2048))
        
        
