import socket

class Communication:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def accept_connection(self):
        client_socket, client_address = self.server_socket.accept()
        return client_socket, client_address

    def send_message(self, encrypted_message, client_socket):
        # Envia a mensagem criptografada pela rede
        client_socket.sendall(encrypted_message.encode('utf-8'))

    def receive_message(self, client_socket):
        # Recebe a mensagem criptografada do outro lado da rede
        data = client_socket.recv(1024)
        received_message = data.decode('utf-8')
        return received_message

    def close_server(self):
        if self.server_socket:
            self.server_socket.close()