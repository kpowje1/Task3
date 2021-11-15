import socket
from _thread import *
import base64
from _datetime import datetime
import os

def multi_threaded_client_p1(connection):
    while True:
        data = connection.recv(2048)
        #Кодирование идентификатора, который ввёл пользователь
        msg = base64.b64encode(data)
        response = 'Server message: Ваш код: '+ msg.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))
        connection.close()
        break
def multi_threaded_client_p2(connection):
    while True:
        data = connection.recv(2048)
        #разделение сообщения, что пришло от пользователя, так как мы отправляли на сервер одним сообщенеим,
        # а не отдельно на каждую переменную
        msg = data.decode('utf-8').split(';')
        #Кодирую идентификатор в base64 чтобы сопоставить с кодом
        id = (base64.b64encode(bytes(msg[0], 'utf-8')).decode('utf-8'))
        code = msg[1]
        if code == id:
             response = 'Server message: ' + 'Код указан верно, сообщение: '+ '"'+ msg[2]+'"' + ' будет записано на сервере'
             print('В лог записано:'+'\n'+'Текст сообщения: ' + msg[2]
                         + '; Идентификатор: ' + msg[0] + '; Возвращенный код: ' + msg[1] + '\n')
             with open(os.path.dirname(os.path.abspath(__file__)) + "/logs.txt", "a") as f:
                 f.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')) + '; Текст сообщения: ' + msg[2]
                         + '; Идентификатор: ' + msg[0] + '; Возвращенный код: ' + msg[1] + '\n')
                 f.close()
        else:
             response = 'Server message: ' + 'Не верно указан код к идентификатору: ' + msg[0] +\
                        '; сообщение не будет записано'
        if not data:
            break
        connection.sendall(str.encode(response))
        connection.close()
        break

def p1():
    Socket = socket.socket()
    host = socket.gethostname()
    try:
        Socket.bind((host, 8000))
    except socket.error as e:
        print(str(e))
    print('Socket is listening..')
    Socket.listen(50)
    while True:
        Client, address = Socket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client_p1, (Client,))
    Socket.close()
def p2():
    Socket = socket.socket()
    host = socket.gethostname()
    try:
        Socket.bind((host, 8001))
    except socket.error as e:
        print(str(e))
    print('Socket is listening..')
    Socket.listen(50)
    while True:
        Client, address = Socket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client_p2, (Client,))
    Socket.close()

#Запуск потоков для каждого порта
start_new_thread(p1,())
start_new_thread(p2,())
while True:
    pass