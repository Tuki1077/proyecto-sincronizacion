import socket
import time

class Client:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path

    def start_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            while True:
                s.sendall(self.path.encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                print("Server response:", response)
                if response.startswith("request aceptado"):
                    break
                time.sleep(1)  # Esperar y reintentar si es necesario

if __name__ == "__main__":
    import sys
    host = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
    client = Client(host, port, path)
    client.start_client()

