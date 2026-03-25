import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 12345

receiving_file = False

def receive(sock):
    global receiving_file
    while True:
        try:
            if receiving_file:
                continue
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break

def main():
    global receiving_file

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    threading.Thread(target=receive, args=(client,), daemon=True).start()

    while True:
        msg = input()
        if msg.startswith("/upload"):
            parts = msg.split(" ")
            if len(parts) < 2:
                print("Format: /upload <filename>")
                continue

            filename = parts[1]

            if not os.path.exists(filename):
                print("File tidak ada di client")
                continue

            client.send(msg.encode())

            if client.recv(1024) == b"READY":
                receiving_file = True

                with open(filename, "rb") as f:
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        client.send(chunk)

                client.send(b"EOF")
                receiving_file = False

                print(client.recv(1024).decode())

        elif msg.startswith("/download"):
            parts = msg.split(" ")
            if len(parts) < 2:
                print("Format: /download <filename>")
                continue

            filename = parts[1]
            client.send(msg.encode())

            response = client.recv(1024)

            if response == b"NOT FOUND":
                print("File tidak ditemukan di server")
            else:
                receiving_file = True

                with open("downloaded_" + filename, "wb") as f:
                    while True:
                        chunk = client.recv(1024)
                        if chunk == b"EOF":
                            break
                        f.write(chunk)

                receiving_file = False
                print("Download selesai")

        else:
            client.send(msg.encode())


if __name__ == "__main__":
    main()