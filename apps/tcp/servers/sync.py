import socket


# AF_INET - сетевой сокет, а не юниксовый
# SOCK_STREAM - сокет для работы с tcp соединением
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen(10)

while True:
    print('Before .accept()')
    client_socket, addr = server_socket.accept()  # blocking
    print('Connection from', addr)

    while True:
        print('Before .recv()')
        request = client_socket.recv(4096)  # blocking

        if not request:
            break
        else:
            print(request)
            response = 'Echo:\n'.encode() + request
            client_socket.send(response)  # blocking пока из буфера отправки не прочитают и он не очистится

    print('Outside inner while loop')
    client_socket.close()

# server_socket.close()
