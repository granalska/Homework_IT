import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen()
print("Socket server працює на 5000")

while True:
    conn, addr = server.accept()
    data = conn.recv(1024)
    print("Отримано:", data.decode())

    conn.close()