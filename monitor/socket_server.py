import socket
import json
import threading

class SocketServer:

    def __init__(self, port, status_data, restart_callback):
        self.port = port
        self.status_data = status_data
        self.restart_callback = restart_callback

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", self.port))
        server.listen(5)

        while True:
            client, _ = server.accept()
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client):
        try:
            data = client.recv(1024).decode()

            if data == "status":
                client.send(json.dumps(self.status_data).encode())

            elif data == "restart":
                self.restart_callback()
                client.send("OK".encode())

        finally:
            client.close()