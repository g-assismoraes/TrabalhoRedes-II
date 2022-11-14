import socket

class ClientTCP():
    def __init__(self):
        self.HEADER = 1024
        self.name = "Mario"
        self.UDP_PORT = 6000
        self.FORMAT = 'utf-8'
        self.UDP_HOST = socket.gethostbyname(socket.gethostname())
        self.UDP_ADDRESS = (self.UDP_HOST, self.UDP_PORT)

        self.SERVER_HOST = "127.0.0.1" # <--------- MUDAR
        self.SERVER_PORT = 5000
        self.SERVER_ADRESS = (self.SERVER_HOST, self.SERVER_PORT)
    
    def start(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.SERVER_ADRESS)
        self.client = client

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        self.client.send(message)
        print(self.client.recv(self.HEADER).decode(self.FORMAT))
    
    def close(self):
        cliente.send(f"DISCONNECT {self.name}")
        print(self.client.recv(self.HEADER).decode(self.FORMAT))
    
    def fetchOtherUserAdress(self, name):
        msg = f"GET {name}".encode(self.FORMAT)
        self.client.send(msg)

        resp = self.client.recv(self.HEADER).decode(self.FORMAT)
        
        if "SUCESSO" in resp:
            tratar = list(resp.split("]"))[1]
            aux = tratar[1:len(tratar)-1].split(",")
            self.ADRESS_TO_CALL = [ aux[0][2:len(aux[0])-1], aux[1][2:len(aux[1])-1]]
            
if '__main__':
    cliente = ClientTCP()
    cliente.start()
    cliente.send(f"REGISTER {cliente.name} {cliente.UDP_HOST} {cliente.UDP_PORT}")

    isAlive = True
    while isAlive:
        flag = int(input("Digite [-1] Encerrar [1] Solicitar Endereço: "))
        if flag == -1:
            cliente.close()
            isAlive = False
        elif flag == 1:
            n = input("Digite o nome de quem deseja saber o endereço:")
            retorno = cliente.fetchOtherUserAdress(n)