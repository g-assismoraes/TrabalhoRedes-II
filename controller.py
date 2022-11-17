import UDP.clienteUDP as clienteUDP
import UDP.servidorUDP as servidorUDP
import TCP.clienteTCP as clienteTCP
import socket
import threading

#TODO: remover
global isAlive 
isAlive = True

def start_listener(my_name, my_addr, my_port, app_client):
    listener = servidorUDP.ServidorUDP(my_name, my_port, isAlive, app_client)
    listener.start_server()

def start_recorder(my_name, my_addr, my_port, recorder):
    addrGetter = clienteTCP.ClientTCP(my_addr, 5000, my_name, my_addr, my_port)
    addrGetter.start()
    addrGetter.send(f"REGISTER {addrGetter.name} {addrGetter.UDP_HOST} {addrGetter.UDP_PORT}")
    isOnline = True

    print("LEMBRE-SE DE DIGITAR UMA TECLA DIFERENTE DE [-1] E [1] PARA LIBERAR O CONTROLE:")
    while isOnline:
        if not recorder.streaming:
            print()
            try:
                flag = int(input(f"Digite [-1]Encerrar [1]Solicitar Endereço [3]PASS: \n"))
            except:
                flag = 3

            if flag == -1:
                addrGetter.close()
                isOnline = False
                isAlive = False
            elif flag == 1:
                print()
                n = input("Digite o nome de quem deseja saber o endereço: ")
                addrToCall = addrGetter.fetchOtherUserAdress(n)
                if addrToCall:
                    recorder.setPair(n, int(addrToCall[1]), addrToCall[0])
                    recorder.sendInvitation()
                else:
                    continue
            else: pass

if '__main__':
    my_name = "pao"
    my_addr = socket.gethostbyname(socket.gethostname())
    my_port = 6002

    recorder = clienteUDP.ClientUDP(my_name, my_port, my_addr)
    recorder.start_socket()

    thread_serverUDP = threading.Thread(target=start_listener, args=(my_name, my_addr, my_port, recorder))
    thread_serverUDP.start()

    thread_cliente = threading.Thread(target=start_recorder, args=(my_name, my_addr, my_port, recorder))
    thread_cliente.start()





