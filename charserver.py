import socket  # Importa el módulo socket para permitir la comunicación de red
import threading  # Importa threading para manejar múltiples hilos
import time  # Importa time para manejar tiempos

# Define una clase para el servidor de chat
class ChatServer:
    def __init__(self, host='localhost', port=12345):
        # Configura el servidor con una dirección y un puerto predeterminados
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []  # Almacena los clientes conectados
        self.client_threads = []  # Almacena los hilos de los clientes

    def start_server(self):
        """Inicia el servidor y acepta conexiones entrantes."""
        # Crea el socket del servidor y lo vincula a la dirección y puerto configurados
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor iniciado en {self.host}:{self.port}")
        
        # Bucle que acepta conexiones de nuevos clientes
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Cliente conectado desde {client_address}")
            # Crea un nuevo hilo para manejar la conexión del cliente
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            self.client_threads.append(client_thread)

    def handle_client(self, client_socket):
        """Gestiona la interacción con un cliente."""
        # Envía un mensaje de bienvenida al cliente
        client_socket.send("¡Bienvenido al chat!\n".encode())
        # Obtiene el nombre del cliente
        client_name = self.get_client_name(client_socket)
        # Agrega el cliente a la lista de clientes
        self.clients.append((client_socket, client_name))
        # Notifica a los demás clientes que un nuevo cliente se ha unido
        self.broadcast(f"{client_name} se ha unido al chat.\n")

        try:
            while True:
                # Recibe un mensaje del cliente
                message = client_socket.recv(1024).decode()
                # Si no hay mensaje o el mensaje es 'salir', termina la conexión
                if not message or message.lower() == 'salir':
                    break
                # Envía el mensaje recibido a los demás clientes
                self.broadcast(f"{client_name}: {message}", client_socket)
        finally:
            # Si el cliente se desconecta, lo elimina de la lista de clientes
            self.remove_client(client_socket, client_name)

    def broadcast(self, message, sender_socket=None):
        """Envía un mensaje a todos los clientes conectados, excepto al remitente (si corresponde)."""
        for client_socket, client_name in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except:
                    # Si hay un error al enviar, elimina al cliente
                    self.remove_client(client_socket, client_name)

    def remove_client(self, client_socket, client_name):
        """Elimina un cliente desconectado de la lista de clientes y cierra la conexión."""
        # Filtra la lista de clientes para eliminar el desconectado
        self.clients = [(sock, name) for sock, name in self.clients if sock != client_socket]
        client_socket.close()
        # Notifica a los demás clientes que el cliente ha dejado el chat
        self.broadcast(f"{client_name} ha dejado el chat.\n")
        print(f"Cliente {client_name} desconectado.")
    
    def get_client_name(self, client_socket):
        """Solicita y devuelve el nombre del cliente."""
        # Solicita al cliente que ingrese su nombre
        client_socket.send("Por favor, ingrese su nombre: ".encode())
        client_name = client_socket.recv(1024).decode().strip()
        return client_name if client_name else f"Usuario_{time.time()}"

# Código principal para iniciar el servidor de chat
if __name__ == "__main__":
    server = ChatServer()
    server.start_server()