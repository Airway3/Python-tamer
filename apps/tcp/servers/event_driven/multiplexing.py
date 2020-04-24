import socket
from select import select


to_monitor = []  # список объектов (сокетов), которые мы мониторим когда они станут доступны для чтения

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))  # создаём файл сокета
server_socket.listen(10)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()  # событие - во входящем буфере данные о новом подключении
    print('Connection from', addr)

    to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)  # событие - во входящем буфере появились данные от клиента

    if request:
        print(request)
        response = 'Echo:\n'.encode() + request
        client_socket.send(response)  # пишет в буфер отправки, событие - очистка буфера отправки,
                                      # т.е. готовность сокета туда что-то записывать
    else:
        to_monitor.remove(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # select - мониторинг изменения состояния файловых объектов, которые в неё передали
        ready_to_read, _, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(server_socket)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
