import socket

class ClientTCP():
    def __init__(self, server_ip, server_port, name, ip=socket.gethostbyname(socket.gethostname()), port=6000):
        #atributos auxiliares
        self.BUFFER = 1024
        self.FORMAT = 'utf-8'
        
        #identificacao do proprio endereco do clienteTCP
        self.name = name
        self.UDP_PORT = port
        self.UDP_HOST = ip
        self.UDP_ADDRESS = (self.UDP_HOST, self.UDP_PORT)

        #identificacao do servidorTCP com quem o clienteTCP ira se conectar
        self.SERVER_HOST = server_ip 
        self.SERVER_PORT = server_port
        self.SERVER_ADRESS = (self.SERVER_HOST, self.SERVER_PORT)
    
    def start(self):
        #inicializa o socket pra conecao TCP
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.SERVER_ADRESS)
        self.client = client

    def send(self, msg):
        #envia a mensagem e espera a resposta
        message = msg.encode(self.FORMAT)
        self.client.send(message)
        print(f"CLIENTE_TCP> Resposta do Servidor: {self.client.recv(self.BUFFER).decode(self.FORMAT)}")
    
    def close(self):
        #envia mensagem ao servidorTCP para de desconectar
        self.send(f"DISCONNECT {self.name}")
       
    def fetchOtherUserAdress(self, name):
        #envia mensagem solicitando o endereço
        if name != self.name: #nao deixa ligar pra si mesmo
            msg = f"GET {name}".encode(self.FORMAT)
            self.client.send(msg)

            #imprime a resposta a solicitacao
            resp = self.client.recv(self.BUFFER).decode(self.FORMAT)
            print(f"CLIENTE_TCP> {resp}")
            
            if "SUCESSO" in resp:
                tratar = list(resp.split("]"))[1]
                aux = tratar[1:len(tratar)-1].split(",")
                self.ADRESS_TO_CALL = [ aux[0][2:len(aux[0])-1], aux[1][2:len(aux[1])-1]]
                return self.ADRESS_TO_CALL
        return None