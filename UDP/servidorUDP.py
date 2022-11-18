import socket 
import threading
import pyaudio


class ServidorUDP():
    def __init__(self, name, port, app_client):
        # parametros auxiliares
        self.FORMAT = 'utf-8'
        self.isAlive = True
        self.isCallOn = False
        self.BUFFER = 2048 * 10
        #o servidorUDP sabe o clienteUDP associado, para quando necessitar parar a ligacao para-lo
        self.app_client = app_client

        # identificacao propria do servidor
        self.MY_NAME = name
        self.MY_UDP_PORT = port
        self.MY_UDP_HOST = socket.gethostbyname(socket.gethostname())
        self.MY_ADRESS = (self.MY_UDP_HOST, self.MY_UDP_PORT)

        # identificacao do cliente que conectou ao servidor
        self.PAIR_NAME = ""
        self.PAIR_UDP_PORT = 6000
        self.PAIR_UDP_HOST = socket.gethostbyname(socket.gethostname())
        self.PAIR_UDP_ADDRESS = ()
        self.PAIR_SERVER_ADRESS = ()

        # parametros para a parte de audio
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
            if (b'ENCERRAR' in data): #encerrar chamada
                #libera os parametros 
                self.isCallOn = False
                self.PAIR_UDP_ADDRESS = ()
                self.PAIR_SERVER_ADRESS = ()

                if self.STREAM != None:self.STREAM.close() #para de ouvir
                self.STREAM=None

                self.app_client.finish_stream() #dispara os comandos para parar a transmissao
            elif (b'CALLBACK' in data) and self.isCallOn == False: #inicializa a segunda parte da chamada quando eh vc mesmo ligando
                #inicializa os modulos de audio
                self.start_listener()
                data_decoded = data.decode(self.FORMAT)

                #seta os enderecos do par conectado
                msgs = list(data_decoded.split(' '))
                self.setPair(msgs[1], addr[1], addr[0])
                self.PAIR_SERVER_ADRESS = (msgs[2], msgs[3])

                self.isCallOn = True
            elif len(data) > 0:
                data_decoded = data.decode(self.FORMAT)
                msgs = list(data_decoded.split(' '))


                if "CONVITE" in data_decoded and self.PAIR_SERVER_ADRESS == (): #recebeu um convite

                    print(f'SERVIDOR_UDP> {self.MY_NAME}, {msgs[1]} te liga!')
                    print()

                    try:
                        r = input("[Y]Atender [N]Recusar: ")
                    except:
                        r = 'N'
                    
                    self.setPair(msgs[1], addr[1], addr[0])
                    self.PAIR_SERVER_ADRESS = (msgs[2], msgs[3])

                    if r.upper() == "Y":
                        self.server.sendto(f'ACEITO'.encode(self.FORMAT), self.PAIR_UDP_ADDRESS)
                        self.isCallOn = True
                        self.start_listener()
                        #dispara para seu cliente iniciar a outra metade da chamada
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
        #inicializa a parte dos sockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(self.MY_ADRESS)

        while self.isAlive:
            data, addr = self.server.recvfrom(self.CHUNK)
            if (b'CONVITE' in data) or (b'ENCERRAR' in data) or (b'CALLBACK' in data): #se for uma mensagem tratavel
                print(f"SERVIDOR_UDP> Uma solicitação chegou: {data} de {addr}")
                print()
                thread = threading.Thread(target=self.serve_client, args=(data, addr))
                thread.daemon = True
                thread.start()
            #se for dado de audio e ja se estiver preparado para trata-los
            elif self.isCallOn and addr == self.PAIR_UDP_ADDRESS and self.STREAM != None:
                self.listen(data)