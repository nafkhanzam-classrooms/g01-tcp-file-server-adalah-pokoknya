import socket
import os

HOST = '0.0.0.0'
PORT = 12345
FILES_DIR = "files"

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[CONNECTED] {addr}")

        while True:
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
                conn.send(f"Echo: {msg}".encode())

        conn.close()
        print(f"[DISCONNECTED] {addr}")

if __name__ == "__main__":
    main()