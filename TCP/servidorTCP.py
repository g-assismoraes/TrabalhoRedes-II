import socket 
import threading


class ServidorRegistro():
    def __init__(self):
        self.HEADER = 64
        self.PORT = 5000
        self.HOST = "127.0.0.1"  # The server's hostname or IP address
        #self.HOST = socket.gethostbyname(socket.gethostname())
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_FLAG = "!DISCONNECT"
        self.tabela_registros = dict()
        self.isAlive = True

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)

        self.server.listen()
        print(f"[SERVIDOR INICIADO] Servidor no IPV4: {self.HOST}")
        print()

        while self.isAlive:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.serve_client, args=(conn, addr))
            thread.start()
            print(f"[CONEXÕES ATIVAS] {threading.active_count()  - 1}")

    def serve_client(self, conn, addr):
        print(f"[NOVA CONEXÃO] {addr} conectado.")

        connected = True
        while connected and self.isAlive:
            data = conn.recv(1024)
            if len(data) > 0:

                data_decoded = data.decode(self.FORMAT)

                if data_decoded == self.DISCONNECT_FLAG:
                    conn.send(f"[SERVIDOR DESCONECTADO] Usuario encerrou conexao!".encode(self.FORMAT))
                    connected = False
                else:
                    msg = list(data_decoded.split(' '))
                    if msg[0] == "GET":
                        self.sendAdress(msg[1], conn)
                    elif len(msg) == 3:
                        self.addOnRegisterTable(msg, conn)
                    else:
                        print("Mensagem com formato invalido recebida!")

        conn.close()
    
    def sendAdress(self, name, conn):
        if not name in self.tabela_registros.keys():
            conn.send(f"[FALHA] Nao ha esse nome nos registros!".encode(self.FORMAT))
            return
        conn.send(f"[SUCESSO] {self.tabela_registros[name]}".encode(self.FORMAT))


    def addOnRegisterTable(self, msg, conn):
        if msg[0] not in self.tabela_registros.keys():
            self.tabela_registros[msg[0]] = (str(msg[1]), str(msg[2]))
            conn.send(f"[REGISTRO] Dados {self.tabela_registros[msg[0]]} recebidos, {msg[0]}!".encode(self.FORMAT))
            print(self.tabela_registros)
        else:
            conn.send(f"[FALHA NO REGISTRO] Usuario ja existente!".encode(self.FORMAT))
    
    #TODO: achar o momento pra chamar isso
    def kill_server(self):
        self.isAlive = False
        

if '__main__':
    seridorRegistro = ServidorRegistro()
    seridorRegistro.start()