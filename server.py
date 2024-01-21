import socket
import time

print('сервер робит')
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('127.0.0.1', 53210))
serv_sock.listen(10)
print('слухаем')

while True:
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)

    while True:
        data = client_sock.recv(333)
        if data == b'test':
            client_sock.sendall(b'true')
            break
            print('отправил тру')
        if data == b'connection':
            print('конекшн')
            a = open('new_signatures.txt', 'r')
            i = a.read().split('\n')
            for j in i:
                client_sock.sendall(j.encode('ascii'))
                time.sleep(0.001)
            client_sock.close()
            print('соединение закрыто')
