import socket
import select
import os

HOST = '0.0.0.0'
PORT = 12345
FILES_DIR = "files"

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
server.setblocking(False)

poller = select.poll()
poller.register(server, select.POLLIN)

fd_map = {server.fileno(): server}
clients = []

def broadcast(msg, sender):
    for c in clients:
        if c != sender:
            c.send(msg)

print(f"[LISTENING] {HOST}:{PORT}")

while True:
    events = poller.poll()

    for fd, flag in events:
        sock = fd_map[fd]

        if sock == server:
            conn, addr = server.accept()
            conn.setblocking(False)
            poller.register(conn, select.POLLIN)
            fd_map[conn.fileno()] = conn
            clients.append(conn)
            print(f"[CONNECTED] {addr}")

        else:
            try:
                data = sock.recv(1024)
                if not data:
                    poller.unregister(fd)
                    clients.remove(sock)
                    sock.close()
                    continue

                msg = data.decode()

                if msg.startswith("/list"):
                    files = os.listdir(FILES_DIR)
                    sock.send(("\n".join(files) or "Folder kosong").encode())

                elif msg.startswith("/upload"):
                    filename = msg.split(" ")[1]
                    filepath = os.path.join(FILES_DIR, filename)

                    sock.send(b"READY")
                    with open(filepath, "wb") as f:
                        while True:
                            chunk = sock.recv(1024)
                            if chunk == b"EOF":
                                break
                            f.write(chunk)

                    sock.send(b"UPLOAD DONE")

                elif msg.startswith("/download"):
                    filename = msg.split(" ")[1]
                    filepath = os.path.join(FILES_DIR, filename)

                    if not os.path.exists(filepath):
                        sock.send(b"NOT FOUND")
                    else:
                        sock.send(b"READY")
                        with open(filepath, "rb") as f:
                            while True:
                                chunk = f.read(1024)
                                if not chunk:
                                    break
                                sock.send(chunk)
                        sock.send(b"EOF")

                else:
                    broadcast(data, sock)

            except:
                poller.unregister(fd)
                if sock in clients:
                    clients.remove(sock)
                sock.close()