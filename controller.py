import UDP.clienteUDP as clienteUDP
import UDP.servidorUDP as servidorUDP
import TCP.clienteTCP as clienteTCP
import socket
import keyboard
import threading
import sys

def start_listener(my_name, my_addr, my_port, app_client):
    #inicializa o módulo servidor UDP, que ira tratar as solicitacoes e receber e reproduzir o audio
    listener = servidorUDP.ServidorUDP(my_name, my_port, app_client)
    listener.start_server()

def start_recorder(my_name, my_addr, my_port, recorder, server_ip):
    #inicializa o módulo cliente TCP, que sera o responsavel por solicitar o endereco para se ligar
    addrGetter = clienteTCP.ClientTCP(server_ip, 5000, my_name, my_addr, my_port)
    addrGetter.start()
    addrGetter.send(f"REGISTER {addrGetter.name} {addrGetter.UDP_HOST} {addrGetter.UDP_PORT}")

    isOnline = True
    printIsLocked = False
    while isOnline:
        if not recorder.streaming:
            if not printIsLocked:
                print()
                print("Pressione [0]Encerrar [1]Solicitar Endereço:")
                printIsLocked = True
            if keyboard.is_pressed('0'):
                addrGetter.close()
                isOnline = False
            elif keyboard.is_pressed('1'): 
                print()
                n = input("Digite o nome de quem deseja saber o endereço: ")
                addrToCall = addrGetter.fetchOtherUserAdress(n)
                if addrToCall: #se o clienteTCP conseguiu recuperar um endereco valido, inicia a ligacao
                    recorder.setPair(n, int(addrToCall[1]), addrToCall[0])
                    recorder.sendInvitation()
                    printIsLocked = False
                else:
                    printIsLocked = False
            else: pass
        else:
            printIsLocked = False

    sys.exit()

if '__main__':
    my_name = input("Digite o seu nome: ")
    my_addr = socket.gethostbyname(socket.gethostname())
    my_port = 6000
    server_ip = input("Digite o endereço IPV4 do Servidor TCP: ")

    #inicializa o clienteUDP, que será quem fará as gravações
    recorder = clienteUDP.ClientUDP(my_name, my_port, my_addr)
    recorder.start_socket()

    #inicializa a thread que irá cuidar da parte listener, que é o servidorUDP
    thread_serverUDP = threading.Thread(target=start_listener, args=(my_name, my_addr, my_port, recorder))
    thread_serverUDP.daemon = True
    thread_serverUDP.start()

    #inicializa a thread que irá cuidar da parte recorder, que é o clienteUDP
    thread_cliente = threading.Thread(target=start_recorder, args=(my_name, my_addr, my_port, recorder, server_ip))
    thread_cliente.start()





