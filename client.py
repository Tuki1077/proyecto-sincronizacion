import socket
import sys
import time

def start_client(ip, port, path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))

        # Recibir confirmación de conexión
        confirmation = client_socket.recv(1024).decode()
        print(f"Recibido: {confirmation}")

        while True:
            # Enviar request al servidor
            print(f"Enviado: {path}")
            client_socket.send(path.encode())

            # Recibir respuesta del servidor
            response = client_socket.recv(1024).decode()
            print(f"Recibido: {response}")

            if "request aceptado" in response:
                break
            else:
                # Esperar antes de reintentar
                time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            if client_socket.fileno() != -1:
                client_socket.close()
        except Exception as e:
            print(f"Error cerrando el socket: {e}")

if _name_ == "_main_":
    if len(sys.argv) != 4:
        print("Uso: ./client.py <ip> <puerto> <path>")
        sys.exit(1)
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
    
    start_client(ip, port, path)
