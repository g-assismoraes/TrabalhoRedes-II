import socket 
import threading


class ServidorRegistro():
    def __init__(self):
        #para parametros auxiliares
        self.FORMAT = 'utf-8'
        self.tabela_registros = dict()
        self.isAlive = True

        #identificacao
        self.PORT = 5000
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.ADDRESS = (self.HOST, self.PORT)

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)

        self.server.listen()
        print(f"[SERVIDOR INICIADO] Servidor iniciado na porta {self.PORT} no endereço IPV4: {self.HOST}")
        print("[AGUARDANDO PEDIDO DE CONEXÃO]")
        print()

        while self.isAlive:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.serve_client, args=(conn, addr))
            thread.start()

    def serve_client(self, conn, addr):
        #metodo iniciado para servir as colicitacoes de um cliente:
        print(f"[NOVA CONEXÃO] {addr} conectado.")

        connected = True
        while connected and self.isAlive:
            data = conn.recv(1024)
            if len(data) > 0:

                data_decoded = data.decode(self.FORMAT)
                
                print()
                print("--------------------------")
                print("MENSAGEM RECEBIDA:")
                print(data_decoded)
                print("--------------------------")
                print()

                msg = list(data_decoded.split(' '))
                if msg[0] == "GET":
                    self.sendAdress(msg[1], conn)
                elif msg[0] == "REGISTER":
                    self.addOnRegisterTable(msg, conn)
                elif msg[0] == "DISCONNECT":
                    conn.send(f"[SERVIDOR DESCONECTADO] Usuario encerrou conexao!".encode(self.FORMAT))
                    if msg[1].upper() in self.tabela_registros.keys():
                        r = self.tabela_registros.pop(msg[1].upper(), "Error")
                        print(self.tabela_registros)
                    connected = False
                else:
                    print("Mensagem com formato invalido recebida!")

        conn.close()
    
    def sendAdress(self, name, conn):
        nameUpper = name.upper()
        if not nameUpper in self.tabela_registros.keys():
            conn.send(f"[FALHA] Nao existe esse nome nos registros!".encode(self.FORMAT))
            return
        conn.send(f"[SUCESSO] {self.tabela_registros[nameUpper]}".encode(self.FORMAT))


    def addOnRegisterTable(self, msg, conn):
        nameUpper = msg[1].upper()
        if nameUpper not in self.tabela_registros.keys():
            self.tabela_registros[nameUpper] = (str(msg[2]), str(msg[3]))
            conn.send(f"[REGISTRO] Dados {self.tabela_registros[nameUpper]} recebidos, {msg[1]}!".encode(self.FORMAT))
            print(self.tabela_registros)
        else:
            conn.send(f"[FALHA NO REGISTRO] Usuario ja existente!".encode(self.FORMAT))
    
    def kill_server(self):
        self.isAlive = False
        

if '__main__':
    seridorRegistro = ServidorRegistro()
    seridorRegistro.start()