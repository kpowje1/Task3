import socket
import sys

ClientMultiSocket = socket.socket()
host = socket.gethostname()
port = sys.argv[1]
def client_program(port):
    try:
        ClientMultiSocket.connect((host, port))
    except socket.error as e:
        print(str(e))
    if port == 8000:
        Input = input('Введите идентификатор: ')
        ClientMultiSocket.send(str.encode(Input))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
        ClientMultiSocket.close()
    else:
        id = input('Введите идентификатор: ')
        code = input('Введите код: ')
        msg = input('Введите сообщение: ')
        ClientMultiSocket.send(str.encode(id + ';' + code + ';' + msg))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
        ClientMultiSocket.close()

def determination_port(port):
    if port == '8000':
        client_program(8000)
    elif port == '8001':
        client_program(8001)
    else:
        port = input('Введён не корректный порт, укажите порт 8000 или 8001: ')
        determination_port(port)

if __name__ == '__main__':
    determination_port(port)