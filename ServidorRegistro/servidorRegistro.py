import socket

class ServidorRegistro():
    def __init__(self):
        self.HOST = "127.0.0.1"  # The server's hostname or IP address
        #self.HOST = socket.gethostbyname(socket.gethostname())
        print(self.HOST)
        self.PORT = 5000  # The port used by the server
        self.tabela_registros = dict()
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server

        server.bind((self.HOST, self.PORT))
        server.listen()

    def open_con(self):
        connected = True
        while connected:
            conn, addr = self.server.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    decoded_data = data.decode("utf-8")
                    if data:
                        self.addOnDict(decoded_data)
                    else:
                        break
                    conn.sendall(data)
    
    def addOnDict(self, msg):
        if msg[0] not in self.tabela_registros.keys():
            msg = list(msg.split(','))
            self.tabela_registros[msg[0]] = (int(msg[1]), int(msg[2]))
            print(self.tabela_registros)
        #TODO notificar usuario


if "__main__":
    server = ServidorRegistro()
    server.start()
    server.open_con()
