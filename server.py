import socket
import threading
from collections import deque
import os
import time
from threading import Semaphore

class Server:
    def __init__(self, port, buffer_size, num_threads):
        self.host = '0.0.0.0'
        self.port = port
        self.buffer = deque(maxlen=buffer_size)
        self.buffer_access = Semaphore(buffer_size)  # Control de acceso al buffer
        self.space_available = Semaphore(buffer_size)  # Control de espacios disponibles
        self.items_available = Semaphore(0)  # Sincronización de items disponibles
        self.threads = [threading.Thread(target=self.handle_requests) for _ in range(num_threads)]

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f'Server listening on port {self.port}')
            for thread in self.threads:
                thread.start()
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.client_connection, args=(conn, addr)).start()

    def client_connection(self, conn, addr):
        print(f"Connection established with {addr}")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            self.process_request(data, conn)

    def process_request(self, path, conn):
        try:
            self.space_available.acquire()
            self.buffer.append((path, conn))
            self.items_available.release()
        except Exception as e:
            conn.sendall("request no aceptado".encode('utf-8'))

    def handle_requests(self):
        while True:
            self.items_available.acquire()
            path, conn = self.buffer.popleft()
            self.space_available.release()
            # Simular procesamiento del folder
            time.sleep(2)
            response = f"Contents of {path} with thread {threading.get_ident()}"
            conn.sendall(response.encode('utf-8'))
            conn.close()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    buffer_size = int(sys.argv[2])
    num_threads = int(sys.argv[3])
    server = Server(port, buffer_size, num_threads)
    server.start_server()
