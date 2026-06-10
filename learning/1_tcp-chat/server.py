# server.py

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 8080))
server.listen()

conn, addr = server.accept()

message_count = 0

while True:
    data = conn.recv(1024)

    if not data:
        break

    msg = data.decode()

    if msg == "quit":
        print("Client disconnected")
        break

    message_count += 1

    print(f"Message #{message_count}: {data.decode()}")
