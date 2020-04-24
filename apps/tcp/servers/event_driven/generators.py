import socket
from select import select
from collections import deque


tasks = deque([])  # queue of generators

to_read = {}  # sock: generator
to_write = {}  # sock: generator


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen(10)

    while True:

        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()  # blocking, read
        print('Connection from', addr)

        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield ('read', client_socket)
        request = client_socket.recv(4096)  # blocking, read

        if not request:
            break
        else:
            print(request)
            response = 'Echo:\n'.encode() + request

            yield ('write', client_socket)
            client_socket.send(response)  # blocking, write

    print('Close client')
    client_socket.close()


def event_loop():
    """ Суть в том что мы вызываем блокирующие операции у тех сокетов которые готовы к работе. """

    while any([tasks, to_read, to_write]):
        ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

        for sock in ready_to_read:
            tasks.append(to_read.pop(sock))

        for sock in ready_to_write:
            tasks.append(to_write.pop(sock))

        while tasks:
            try:
                task = tasks.popleft()

                reason, sock = next(task)

                if reason == 'read':
                    to_read[sock] = task
                if reason == 'write':
                    to_write[sock] = task

            except StopIteration:
                print('Queue Empty')


if __name__ == '__main__':
    server_gen = server()
    _, sock = next(server_gen)

    to_read[sock] = server_gen

    event_loop()
