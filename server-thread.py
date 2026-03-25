import socket
import threading
import os

HOST = '0.0.0.0'
PORT = 12345
clients = []
FILES_DIR = "files"

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    clients.append(conn)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode()

            if msg.startswith("/list"):
                files = os.listdir(FILES_DIR)
                conn.send(("\n".join(files) or "Folder kosong").encode())

            elif msg.startswith("/upload"):
                filename = msg.split(" ")[1]
                filepath = os.path.join(FILES_DIR, filename)

                conn.send(b"READY")
                with open(filepath, "wb") as f:
                    while True:
                        chunk = conn.recv(1024)
                        if chunk == b"EOF":
                            break
                        f.write(chunk)

                conn.send(b"UPLOAD DONE")

            elif msg.startswith("/download"):
                filename = msg.split(" ")[1]
                filepath = os.path.join(FILES_DIR, filename)

                if not os.path.exists(filepath):
                    conn.send(b"NOT FOUND")
                else:
                    conn.send(b"READY")
                    with open(filepath, "rb") as f:
                        while True:
                            chunk = f.read(1024)
                            if not chunk:
                                break
                            conn.send(chunk)
                    conn.send(b"EOF")

            else:
                broadcast(data, conn)

        except:
            break

    clients.remove(conn)
    conn.close()
    print(f"[DISCONNECTED] {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()