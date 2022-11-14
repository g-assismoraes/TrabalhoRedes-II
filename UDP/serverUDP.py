import socket
import pyaudio
import threading
from os import system

system('clear')

# Socket
host = socket.gethostbyname(socket.gethostname())
port = 6000
buffer = 2048 * 10
clients = []

# Audio
audio = pyaudio.PyAudio()
chunk = int(1024 * 4)


def client_listener():
    while True:
        data, address = host_socket.recvfrom(buffer)
        if address not in clients:
            print(f'New client: {address[0]}:{address[1]}')
            clients.append(address)
            print(clients)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as host_socket:
    try:
        host_socket.bind((host, port))
        print(f'Server hosted at {host}:{port}\n')

        print('Starting listener thread...')
        listener_thread = threading.Thread(target=client_listener)
        listener_thread.daemon = True
        listener_thread.start()
        print('Listener thread started!')

        print('Initiating microphone...')
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=chunk)

        print('Recording!')
        while True:
            voice_data = stream.read(chunk, exception_on_overflow=False)
            for client in clients:
                host_socket.sendto(voice_data, client)
    except socket.error as error:
        print(str(error))
        stream.close()
        host_socket.close()
    except KeyboardInterrupt:
        stream.close()
        host_socket.close()
    finally:
        stream.close()
        host_socket.close()