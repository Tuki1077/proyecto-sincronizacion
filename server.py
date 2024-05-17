import socket
import threading
import queue
import os
import sys
import time

def handle_client(client_socket, buffer, empty, full):
    try:
        # Enviar confirmación de conexión al cliente
        client_socket.send(f"Comunicación con ip {client_socket.getpeername()[0]} y puerto {client_socket.getsockname()[1]}".encode())

        while True:
            # Recibir solicitud del cliente
            request = client_socket.recv(1024).decode()  # Recibe hasta 1024 bytes
            if request:
                # Intentar agregar la solicitud al buffer
                if empty.acquire(blocking=False):  # Adquirir un espacio vacío sin bloquear
                    buffer.put((request, client_socket))  # Poner la solicitud y el socket en el buffer
                    full.release()  # Liberar un espacio lleno
                    print(f"Request aceptado: {request}, buffer size: {buffer.qsize()}")
                    client_socket.send(f"request aceptado, y almacenado en la casilla del buffer numero {buffer.qsize()}".encode())
                    break  # Salir del bucle después de aceptar la solicitud
                else:
                    # Si el buffer está lleno, rechazar la solicitud
                    print("Buffer lleno, request no aceptado")
                    client_socket.send("request no aceptado".encode())
                    time.sleep(1)  # Esperar antes de reintentar
            else:
                break  # Salir del bucle si no hay solicitud
    except Exception as e:
        # Manejo de excepciones para errores durante la conexión o transmisión de datos
        print(f"Error handling client: {e}")
    finally:
        pass  # No cerramos el socket aquí para mantener la conexión abierta

def consumer(buffer, empty, full):
    while True:
        full.acquire()  # Espera a que haya un elemento en el buffer
        request, client_socket = buffer.get()  # Obtener la solicitud y el socket del buffer
        empty.release()  # Liberar un espacio vacío
        print(f"Procesando request: {request}, buffer size: {buffer.qsize()}")

        # Procesar la solicitud (listar el contenido del folder)
        try:
            folder_content = os.listdir(request)  # Obtener el contenido del directorio
            thread_name = threading.current_thread().name  # Obtener el nombre del hilo actual
            # Crear la respuesta con el nombre del hilo y el contenido del directorio
            response = f"Thread {thread_name} processed request. Folder contents: {folder_content}"

            # Enviar la respuesta al cliente
            client_socket.send(response.encode())
            print(f"Enviando respuesta: {response}")  # Agregar mensaje de depuración
        except Exception as e:
            # Manejo de excepciones para errores al procesar la solicitud
            print(f"Error processing request: {e}")
        finally:
            try:
                if client_socket.fileno() != -1:
                    client_socket.close()  # Cerramos el socket después de enviar la respuesta
                    print(f"Conexión cerrada con el cliente")
            except Exception as e:
                # Manejo de excepciones para errores al cerrar el socket
                print(f"Error cerrando el socket: {e}")

def Server(port, buffer_size, num_threads):
    # Crear una cola para manejar el buffer de solicitudes
    buffer = queue.Queue(buffer_size)
    # Crear semáforos para controlar el acceso al buffer
    empty = threading.Semaphore(buffer_size)  # Inicialmente, el buffer está vacío
    full = threading.Semaphore(0)  # Inicialmente, no hay elementos en el buffer

    # Crear y configurar el socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))  # Cambiar a '0.0.0.0' para escuchar en todas las interfaces
    server_socket.listen(5)  # Escuchar hasta 5 conexiones entrantes
    print(f"Servidor escuchando en el puerto {port}")

    # Crear hilos consumidores para procesar las solicitudes del buffer
    for _ in range(num_threads):
        thread = threading.Thread(target=consumer, args=(buffer, empty, full))
        thread.daemon = True  # Hacer que los hilos sean daemon para que terminen con el programa principal
        thread.start()

    while True:
        # Aceptar conexiones entrantes de clientes
        client_socket, addr = server_socket.accept()
        print(f"Conexión aceptada de {addr}")
        # Crear un hilo para manejar la conexión con el cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, buffer, empty, full))
        client_handler.start()

if __name__ == "__main__":
    # Verificar que se hayan proporcionado los argumentos correctos (puerto, tamaño del buffer, número de hilos)
    if len(sys.argv) != 4:
        print("Uso: ./server.py <puerto> <elementos en buffer> <hilos>")
        sys.exit(1)  # Salir del programa si no se proporcionan los argumentos correctos
    
    # Asignar los argumentos a variables
    port = int(sys.argv[1])
    buffer_size = int(sys.argv[2])
    num_threads = int(sys.argv[3])
    
    # Iniciar el servidor con los parámetros proporcionados
    Server(port, buffer_size, num_threads)
