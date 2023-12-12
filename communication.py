import socket
import pickle

class Communication:
    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", self.port))

    def send_message(self, destination, message):
        serialized_message = pickle.dumps(message)
        self.socket.sendto(serialized_message, destination)

    def receive_message(self):
        data, _ = self.socket.recvfrom(1024)
        message = pickle.loads(data)
        return message
