import socket

HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 8888         # Puerto en el que el servidor estará escuchando

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlaza el socket a la dirección y puerto especificados
server_socket.bind((HOST, PORT))

# Pone el socket en modo de escucha
server_socket.listen(1)

print(f"Servidor escuchando en {HOST}:{PORT}")

# Acepta conexiones entrantes
client_socket, client_address = server_socket.accept()

print(f"Conexión establecida desde {client_address}")

# Lee los datos enviados desde Unity
data = client_socket.recv(1024)

# Procesa los datos, realiza el análisis de audio y envía los resultados de vuelta a Unity

# Cierra los sockets
client_socket.close()
server_socket.close()
