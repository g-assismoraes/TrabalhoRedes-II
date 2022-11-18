import socket
import pyaudio
import keyboard

class ClientUDP():
    def __init__(self, myname, myport, myhost): 
        #parametros auxiliares
        self.BUFFER = 2048 * 10
        self.streaming = False
        self.FORMAT = 'utf-8'

        #informacoes de identificacao do meu proprio servidorUDP
        self.MY_NAME = myname
        self.MY_UDP_PORT = myport
        self.MY_UDP_HOST = myhost
        self.MY_ADRESS = (myhost, myport)

        #informacoes de do par que esta em chamada com
        self.PAIR_NAME = ""
        self.PAIR_UDP_PORT = 6000
        self.PAIR_UDP_HOST = "" 
        self.PAIR_UDP_ADDRESS = (self.PAIR_UDP_HOST, self.PAIR_UDP_PORT)

        # parametros para a parte de audio
        self.AUDIO = pyaudio.PyAudio()
        self.CHUNK = int(1024 * 4)

    def start_socket(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client = client
    
    def setPair(self, name, port, ip):
        self.PAIR_NAME = name
        self.PAIR_UDP_PORT = port
        self.PAIR_UDP_HOST = ip 
        self.PAIR_UDP_ADDRESS = (ip, port)
    
    def start_call_back(self, name, addr):
        #envia o comando para fazer a segunda metade da ligacao e iniciar o gravador
        self.setPair(name, int(addr[1]), addr[0])
        self.client.sendto(f"CALLBACK {name} {addr[0]} {addr[1]}".encode(self.FORMAT), self.PAIR_UDP_ADDRESS)
        self.start_stream()


    def sendInvitation(self):
        self.client.sendto(f"CONVITE {self.MY_NAME} {self.MY_UDP_HOST} {self.MY_UDP_PORT}".encode(self.FORMAT), self.PAIR_UDP_ADDRESS)
        answer = self.client.recvfrom(self.BUFFER)

        answer = answer[0].decode(self.FORMAT)


        if "ACEITO" in answer:
            print(f"CLIENTE_UDP> {answer}")
            print()
            self.start_stream()
        else: 
            print("CLIENTE_UDP> Usuario destino ocupado!")
            print()
    
    def finish_stream(self):
        self.streaming = False
        self.sending=False
        if self.STREAM.is_active:
            self.STREAM.close()
    
    def start_stream(self):
        #inicializa os parametros de audio
        self.STREAM = self.AUDIO.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=self.CHUNK)
        self.streaming = True

        try:
            print('CLIENTE_UDP> Chmada inicializada! Digite "]" para encerrar.')
            print()
            self.sending = True
            while self.sending:
                if keyboard.is_pressed(']'):
                    print("CLIENTE_UDP> encerrando chamada...")
                    print()
                    self.STREAM.close()
                    self.streaming = False
                    self.sending = False
                    self.client.sendto(b"ENCERRAR", self.PAIR_UDP_ADDRESS)
                    self.client.sendto(b"ENCERRAR", self.MY_ADRESS)
            
                if self.streaming:
                    voice_data = self.STREAM.read(self.CHUNK, exception_on_overflow=False)
                    self.client.sendto(voice_data, self.PAIR_UDP_ADDRESS)

        except socket.error as error:
            print(str(error))
            self.STREAM.close()
            self.client.close()
