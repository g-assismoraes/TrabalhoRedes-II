import socket 
import threading
import pyaudio
import keyboard


class ServidorUDP():
    def __init__(self, name, port, flag, app_client):
        self.MY_NAME = name
        self.MY_UDP_PORT = port
        self.MY_UDP_HOST = socket.gethostbyname(socket.gethostname())
        self.MY_ADRESS = (self.MY_UDP_HOST, self.MY_UDP_PORT)

        self.FORMAT = 'utf-8'
        self.isAlive = flag
        self.BUFFER = 2048 * 10

        self.isCallOn = False
        self.app_client = app_client

        self.PAIR_NAME = ""
        self.PAIR_UDP_PORT = 6000
        self.FORMAT = 'utf-8'
        self.PAIR_UDP_HOST = socket.gethostbyname(socket.gethostname())
        self.PAIR_UDP_ADDRESS = ()
        self.PAIR_SERVER_ADRESS = ()

        # Audio
        self.STREAM = None
        self.AUDIO = pyaudio.PyAudio()
        self.CHUNK = int(1024 * 10)
    
    def setPair(self, name, port, ip):
        self.PAIR_NAME = name
        self.PAIR_UDP_PORT = port
        self.PAIR_UDP_HOST = ip 
        self.PAIR_UDP_ADDRESS = (ip, port)
    
    def serve_client(self, data, addr):

        if self.isAlive:
            if (b'ENCERRAR' in data):
                self.isCallOn = False
                self.PAIR_UDP_ADDRESS = ()
                self.PAIR_SERVER_ADRESS = ()
                if self.STREAM != None:self.STREAM.close() #para de ouvir
                self.STREAM=None
                self.app_client.finish_stream() #para de transmitir
            elif (b'SUPERCONV' in data) and self.isCallOn == False:
                self.start_listener()
                data_decoded = data.decode(self.FORMAT)
                msgs = list(data_decoded.split(' '))
                self.setPair(msgs[1], addr[1], addr[0])
                self.PAIR_SERVER_ADRESS = (msgs[2], msgs[3])
                self.isCallOn = True
            elif len(data) > 0:
                data_decoded = data.decode(self.FORMAT)
                msgs = list(data_decoded.split(' '))
                if "CONVITE" in data_decoded and self.PAIR_SERVER_ADRESS == ():
                    print(f'SERVERUDP> {self.MY_NAME}, {msgs[1]} te liga!')
                    print()
                    r = int(input("[1]Atender [2]Recusar: "))
                    self.setPair(msgs[1], addr[1], addr[0])
                    self.PAIR_SERVER_ADRESS = (msgs[2], msgs[3])
                    if r == 1:
                        self.server.sendto(f'ACEITO'.encode(self.FORMAT), self.PAIR_UDP_ADDRESS)
                        self.isCallOn = True
                        self.start_listener()
                        self.app_client.start_call_back(msgs[1], self.PAIR_SERVER_ADRESS)
                    else:
                        self.server.sendto(f'REJEITADO'.encode(self.FORMAT), self.PAIR_UDP_ADDRESS)
                        self.PAIR_UDP_ADDRESS = ()
                        self.PAIR_SERVER_ADRESS = ()
                elif "CONVITE" in data_decoded:
                    self.server.sendto(f'REJEITADO'.encode(self.FORMAT), (addr[0], addr[1]))
                

    def start_listener(self):
        self.STREAM = self.AUDIO.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=44100,
                                output=True,
                                frames_per_buffer=self.CHUNK)

    def listen(self, voice_data):
        try:
            self.STREAM.write(voice_data)
        except socket.error as error:
            print(str(error))
            self.STREAM.close()
            self.STREAM=None
            self.server.close()

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(self.MY_ADRESS)

        # print(f"[SERVIDOR INICIADO] Servidor no IPV4: {self.MY_UDP_HOST}")
        # print()

        #TODO:matar ele em algum momento
        while self.isAlive:
            data, addr = self.server.recvfrom(self.CHUNK)
            if (b'CONVITE' in data) or (b'ENCERRAR' in data) or (b'SUPERCONV' in data): #tratar
                print(f"SERVIDORUDP> {data}")
                print()
                thread = threading.Thread(target=self.serve_client, args=(data, addr))
                thread.daemon = True
                thread.start()
            elif self.isCallOn and addr == self.PAIR_UDP_ADDRESS and self.STREAM != None:
                self.listen(data)

# if "__main__":
#     servidor = ServidorUDP()
#     servidor.start_server()