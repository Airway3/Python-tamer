import os
import sys
import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen(10)


for i in range(4):
    child_pid = os.fork()  # linux only

    if child_pid == 0:
        try:
            while True:
                print('Before .accept()')
                client_socket, addr = server_socket.accept()
                print('Connection from', addr)

                while True:
                    print('Before .recv()')
                    request = client_socket.recv(4096)

                    if not request:
                        break
                    else:
                        print(request)
                        response = 'Echo:\n'.encode() + request
                        client_socket.send(response)

                client_socket.close()
        except KeyboardInterrupt:
            sys.exit()


try:
    os.waitpid(-1, 0)
except KeyboardInterrupt:
    sys.exit()
