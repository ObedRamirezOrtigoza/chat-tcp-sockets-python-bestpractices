import socket
import threading

class ChatClient:
    def __init__(self, server_host='localhost', server_port=12345):
        # Configura el cliente con la dirección del servidor y el puerto
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = None

    def start_client(self):
        """Conecta al cliente al servidor y empieza a enviar y recibir mensajes."""
        # Crea el socket del cliente y se conecta al servidor
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

        # Recibe el mensaje de bienvenida del servidor
        print(self.client_socket.recv(1024).decode())

        # Inicia un hilo para recibir mensajes del servidor
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # Bucle principal para enviar mensajes al servidor
        while True:
            message = input("")
            self.client_socket.send(message.encode())

    def receive_messages(self):
        """Recibe y muestra mensajes del servidor."""
        while True:
            try:
                # Recibe un mensaje y lo muestra
                message = self.client_socket.recv(1024).decode()
                print(message)
            except:
                break

# Código principal para iniciar el cliente de chat
if __name__ == "__main__":
    client = ChatClient()
    client.start_client()