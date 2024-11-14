# Chat en Python con Sockets y Multihilos

Este repositorio contiene el código para un sencillo servidor y cliente de chat en Python. La comunicación se maneja mediante sockets y threads, lo que permite la conexión de múltiples clientes a un servidor y el envío de mensajes entre ellos en tiempo real.

## Descripción del Proyecto

El sistema de chat está compuesto por dos componentes:
1. **Servidor de Chat (`Charserver`)**: Actúa como intermediario, gestionando las conexiones de los clientes y retransmitiendo los mensajes a todos los usuarios conectados.
2. **Cliente de Chat (`cliente`)**: Se conecta al servidor y permite a un usuario enviar y recibir mensajes de otros participantes del chat.

## Características

- **Conexiones simultáneas**: Permite que varios clientes se conecten y chateen entre sí de forma simultánea.
- **Mensajes de bienvenida y notificación**: El servidor envía un mensaje de bienvenida a cada cliente al unirse, y notifica a todos los usuarios cuando alguien entra o sale del chat.
- **Hilos independientes para cada cliente**: La comunicación de cada cliente se maneja en un hilo separado, manteniendo el flujo de mensajes constante y sin interrupciones.
  
## Estructura del Código

### ChatServer

- **start_server**: Inicia el servidor, acepta conexiones entrantes y crea un hilo para cada cliente conectado.
- **handle_client**: Gestiona la comunicación con un cliente individual, incluyendo la recepción y retransmisión de mensajes.
- **broadcast**: Envía mensajes a todos los clientes conectados, excepto al remitente.
- **remove_client**: Maneja la desconexión de un cliente y notifica a los demás.
- **get_client_name**: Solicita el nombre del cliente al conectarse.

### ChatClient

- **start_client**: Conecta el cliente al servidor y comienza los hilos para enviar y recibir mensajes.
- **receive_messages**: Recibe y muestra mensajes del servidor.
