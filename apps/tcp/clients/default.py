import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5000))

request = input()
s.send(request.encode())

response = s.recv(4096)
print(response.decode())
s.close()
