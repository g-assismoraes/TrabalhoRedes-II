import socket
import pyaudio
from os import system

# Socket
host = socket.gethostbyname(socket.gethostname())
print(host)
port = 6000

#system('clear')

# Audio
audio = pyaudio.PyAudio()
chunk = int(1024 * 10)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    try:
        client_socket.sendto(' '.encode('utf-8'), (host, port))

        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            output=True,
                            frames_per_buffer=chunk)

        while True:
            voice_data = client_socket.recv(chunk)
            print(voice_data)
            stream.write(voice_data)
    except socket.error as error:
        print(str(error))
        stream.close()
        client_socket.close()
    except KeyboardInterrupt:
        stream.close()
        client_socket.close()
    finally:
        stream.close()
        client_socket.close()