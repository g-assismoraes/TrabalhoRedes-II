import UDP.clienteUDP as clienteUDP
import UDP.servidorUDP as servidorUDP
import TCP.clienteTCP as clienteTCP
import socket
import keyboard
import threading
import sys

def start_listener(my_name, my_addr, my_port, app_client):
    listener = servidorUDP.ServidorUDP(my_name, my_port, app_client)
    listener.start_server()

def start_recorder(my_name, my_addr, my_port, recorder, server_ip):
    addrGetter = clienteTCP.ClientTCP(server_ip, 5000, my_name, my_addr, my_port)
    addrGetter.start()
    addrGetter.send(f"REGISTER {addrGetter.name} {addrGetter.UDP_HOST} {addrGetter.UDP_PORT}")
    isOnline = True
    printIsLocked = False
    while isOnline:
        if not recorder.streaming:
            if not printIsLocked:
                print()
                print("Digite [0]Encerrar [1]Solicitar Endereço: \n")
                printIsLocked = True
            if keyboard.is_pressed('3'): #flag == -1:
                addrGetter.close()
                isOnline = False
            elif keyboard.is_pressed('4'): #flag == 1:
                print()
                n = input("Digite o nome de quem deseja saber o endereço: ")
                addrToCall = addrGetter.fetchOtherUserAdress(n)
                if addrToCall:
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
    my_name = "gabriel"
    my_addr = socket.gethostbyname(socket.gethostname())
    my_port = 6000
    server_ip = '192.168.0.6'

    recorder = clienteUDP.ClientUDP(my_name, my_port, my_addr)
    recorder.start_socket()

    thread_serverUDP = threading.Thread(target=start_listener, args=(my_name, my_addr, my_port, recorder))
    thread_serverUDP.daemon = True
    thread_serverUDP.start()

    thread_cliente = threading.Thread(target=start_recorder, args=(my_name, my_addr, my_port, recorder, server_ip))
    thread_cliente.start()





