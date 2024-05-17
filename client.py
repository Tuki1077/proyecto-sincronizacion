import socket  # Importa el módulo socket para crear conexiones de red
import sys     # Importa el módulo sys para manejar argumentos y funciones del sistema
import time    # Importa el módulo time para usar funciones de tiempo, como sleep

def start_client(ip, port, path):
    # Crear un socket para el cliente usando TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Conectar el socket del cliente al servidor especificado por la IP y el puerto
        client_socket.connect((ip, port))

        # Recibir confirmación de conexión desde el servidor
        confirmation = client_socket.recv(1024).decode()  # Recibe hasta 1024 bytes
        print(f"Recibido: {confirmation}")  # Imprime la confirmación de conexión

        while True:
            # Enviar la solicitud (path) al servidor
            print(f"Enviado: {path}")
            client_socket.send(path.encode())  # Envía la ruta al servidor codificada en bytes

            # Recibir respuesta del servidor
            response = client_socket.recv(1024).decode()  # Recibe hasta 1024 bytes
            print(f"Recibido: {response}")  # Imprime la respuesta del servidor

            if "request aceptado" in response:
                # Si la solicitud fue aceptada, esperar y recibir el contenido del folder
                folder_response = client_socket.recv(4096).decode()  # Recibe hasta 4096 bytes
                print(f"Contenido del folder recibido: {folder_response}")  # Imprime el contenido del folder
                break  # Salir del bucle ya que la solicitud fue procesada correctamente
            else:
                # Si la solicitud no fue aceptada, esperar 1 segundo antes de reintentar
                time.sleep(1)

    except Exception as e:
        # Manejo de excepciones para errores durante la conexión o transmisión de datos
        print(f"Error: {e}")
    finally:
        try:
            # Cerrar el socket si aún está abierto
            if client_socket.fileno() != -1:
                client_socket.close()
        except Exception as e:
            # Manejo de excepciones para errores al cerrar el socket
            print(f"Error cerrando el socket: {e}")

if _name_ == "_main_":
    # Verificar que se hayan proporcionado 3 argumentos (ip, puerto y path)
    if len(sys.argv) != 4:
        print("Uso: ./client.py <ip> <puerto> <path>")
        sys.exit(1)  # Salir del programa si no se proporcionan los argumentos correctos
    
    # Asignar los argumentos a variables
    ip = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
    
    # Iniciar el cliente con los parámetros proporcionados
    start_client(ip, port, path)
