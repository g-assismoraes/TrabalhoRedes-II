import socket
import pyaudio
import keyboard

class ClientUDP():
    def __init__(self, myname, myport, myhost): 
        self.MY_NAME = myname
        self.MY_UDP_PORT = myport
        self.MY_UDP_HOST = myhost
        self.MY_ADRESS = (myhost, myport)

        self.PAIR_NAME = ""
        self.PAIR_UDP_PORT = 6000
        self.FORMAT = 'utf-8'
        self.PAIR_UDP_HOST = "127.0.0.1" #socket.gethostbyname(socket.gethostname())
        self.PAIR_UDP_ADDRESS = (self.PAIR_UDP_HOST, self.PAIR_UDP_PORT)

        self.BUFFER = 2048 * 10

        self.streaming = False

        # Audio
        self.AUDIO = pyaudio.PyAudio()
        self.CHUNK = int(1024 * 4)

        self.pairs = []

    def start_socket(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client = client
    
    def setPair(self, name, port, ip):
        self.PAIR_NAME = name
        self.PAIR_UDP_PORT = port
        self.PAIR_UDP_HOST = ip 
        self.PAIR_UDP_ADDRESS = (ip, port)
    
    def start_call_back(self, name, addr):
        self.setPair(name, int(addr[1]), addr[0])
        self.client.sendto(f"SUPERCONV {name} {addr[0]} {addr[1]}".encode(self.FORMAT), self.PAIR_UDP_ADDRESS)
        self.start_stream()


    def sendInvitation(self):
        self.client.sendto(f"CONVITE {self.MY_NAME} {self.MY_UDP_HOST} {self.MY_UDP_PORT}".encode(self.FORMAT), self.PAIR_UDP_ADDRESS)
        answer = self.client.recvfrom(self.BUFFER)

        answer = answer[0].decode(self.FORMAT)


        if "ACEITO" in answer:
            print(f"CLIENTEUDP> {answer}")
            print()
            self.start_stream()
        else: 
            print("CLIENTEUDP> Usuario destino ocupado!")
            print()
    
    def finish_stream(self):
        self.streaming = False
        self.sending=False
        if self.STREAM.is_active:
            self.STREAM.close()
    
    def start_stream(self):
        self.STREAM = self.AUDIO.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=self.CHUNK)
        self.streaming = True

        try:
            print('CLIENTEUDP> Recording!')
            print()
            self.sending = True
            while self.sending:
                if keyboard.is_pressed(']'):
                    self.client.sendto(b"ENCERRAR", self.PAIR_UDP_ADDRESS)
                    self.client.sendto(b"ENCERRAR", self.MY_ADRESS)
                    print("CLIENTEUDP> encerrando chamada...")
                    print()
                    self.STREAM.close()
                    self.streaming = False
                    self.sending = False
            
                if self.streaming:
                    voice_data = self.STREAM.read(self.CHUNK, exception_on_overflow=False)
                    self.client.sendto(voice_data, self.PAIR_UDP_ADDRESS)

        except socket.error as error:
            print(str(error))
            self.STREAM.close()
            self.client.close()

# if "__main__":
#     cliente = ClientUDP("Gabriel", 6000, '127.0.0.1')
#     cliente.start_socket()
#     cliente.setPair("Gabriel", 6000, '127.0.0.1')
#     cliente.sendInvitation()