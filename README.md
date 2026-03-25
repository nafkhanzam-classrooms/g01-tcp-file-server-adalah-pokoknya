[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mRmkZGKe)
# Network Programming - Assignment G01

## Anggota Kelompok
| Nama                     | NRP        | Kelas |
|--------------------------|------------|-------|
| Umi Lailatul Khotimah    | 5025241062 |   C   |
| Nashwa Aulia Putri D     | 5025241064 |   C   |

## Link Youtube (Unlisted)
Link ditaruh di bawah ini
```

```

## Penjelasan Program
### A. Client.py
### B. Server-thread.py
### C. Server-sync.py
### D. Server-select.py
Server select adalah server yang menangani banyak client dalam satu thread dengan memantau banyak socket menggunakan fungsi select, sehingga lebih efisien tetapi dapat mengalami blocking saat proses tertentu

```
import socket
import select
import os
```
Program diatas untuk mengimpor library yang digunakan untuk komunikasi jaringan(socket), menangani banyak koneksi sekaligus(select), dan mengelola file(os)
```
HOST = '0.0.0.0'
PORT = 12345
FILES_DIR = "files"
```
Digunakan untuk menentukan alamat server, port komunikasi, dan folder penyimpanan file
```
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)
```
Lalu program memastikan folder files tersedia untuk menyimpan file upload
```
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
server.setblocking(False)
```
Setelah itu membuat server TCP, menghubungkan ke host dan port, lalu mengatur socket menjadi non-blocking agar tidak berhenti saat menunggu data
```
sockets = [server]
clients = []
```
Sockets digunakan untuk dipantau oleh select, sedangkan clients menyimpan semua client yang terhubung
```
def broadcast(msg, sender):
    for c in clients:
        if c != sender:
            c.send(msg)
```
Ada program broadcast yang fungsinya sendiri mengirim pesan ke semua client kecuali pengirim
```
while True:
    read_sockets, _, _ = select.select(sockets, [], [])
```
Server terus berjalan dan memeriksa socket yang aktif menggunakan select
```
if sock == server:
    conn, addr = server.accept()
    conn.setblocking(False)
```
Jika ada client baru, server menerima koneksi dan menambahkannya ke daftar
```
data = sock.recv(1024)
files = os.listdir(FILES_DIR)
sock.send(b"READY")
broadcast(data, sock)
```
Server membaca data dari client, jika kosong maka client dianggap disconnect. Menampilkan daftar file yang ada di server dengan perintah list. Server menerima file dari client dan menyimpannya hingga menerima penanda EOF serta mengirim file ke client jika tersedia, lalu diakhiri dengan EOF. Lalu broadcast yang artinya bahwa pesan biasa akan dikirim ke semua client lain
```
except:
    sock.close()
```
Terakhir jika terjadi error, koneksi client akan ditutup.

### E. Server-poll.py
Server poll adalah server yang menangani banyak client dalam satu thread menggunakan mekanisme poll yang lebih efisien daripada select, namun masih dapat mengalami blocking saat proses tertentu
```
import socket
import select
import os

HOST = '0.0.0.0'
PORT = 12345
FILES_DIR = "files"
```
Program ini mengimpor library untuk jaringan, polling, dan file, serta menentukan alamat server, port, dan folder penyimpanan file
```
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)
```
Lalu program memastikan folder files tersedia untuk menyimpan file upload
```
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
server.setblocking(False)
```
Server dibuat menggunakan TCP, di-bind ke alamat dan port, lalu dibuat non-blocking agar bisa menangani banyak client
```
poller = select.poll()
poller.register(server, select.POLLIN)

fd_map = {server.fileno(): server}
clients = []
```
Program ini adalah inti dari server poll, poller digunakan untuk memonitor banyak socket. Server didaftarkan agar bisa dideteksi saat ada koneksi masuk. fd_map digunakan untuk menghubungkan file descriptor ke socket, dan clients menyimpan client aktif
```
def broadcast(msg, sender):
    for c in clients:
        if c != sender:
            c.send(msg)
```
Ada program broadcast yang fungsinya sendiri mengirim pesan ke semua client kecuali pengirim
```
while True:
    events = poller.poll()
```
Server berjalan terus dan menggunakan poll() untuk mendeteksi socket yang sedang aktif
```
if sock == server:
    conn, addr = server.accept()
    conn.setblocking(False)
    poller.register(conn, select.POLLIN)
    fd_map[conn.fileno()] = conn
    clients.append(conn)
```
Jika ada client baru, server menerima koneksi, lalu menambahkannya ke sistem polling dan daftar client
```
data = sock.recv(1024)
if not data:
    poller.unregister(fd)
    clients.remove(sock)
    sock.close()

files = os.listdir(FILES_DIR)
sock.send(b"READY")
broadcast(data, sock)
```
Server membaca data dari client, jika kosong maka client dianggap disconnect. Menampilkan daftar file yang ada di server dengan perintah list. Server menerima file dari client dan menyimpannya hingga menerima penanda EOF serta mengirim file ke client jika tersedia, lalu diakhiri dengan EOF. Lalu broadcast yang artinya bahwa pesan biasa akan dikirim ke semua client lain
```
except:
    poller.unregister(fd)
    sock.close()
```
Terakhir jika terjadi error, socket akan dihapus dari polling dan ditutup

## Screenshot Hasil
### 1. Server thread
<img width="1864" height="474" alt="Screenshot 2026-03-25 144434" src="https://github.com/user-attachments/assets/8394fbb0-8442-4957-922f-f30d8ab99027" />

### 2. Server sync
<img width="1864" height="489" alt="Screenshot 2026-03-25 144737" src="https://github.com/user-attachments/assets/6bc39e8f-aef9-462c-b2db-b63de4f713f7" />

### 3. Server select
<img width="1919" height="571" alt="Screenshot 2026-03-25 144939" src="https://github.com/user-attachments/assets/e4ade567-539c-40a2-af12-89c41e7e1382" />

### 4. Server poll
<img width="1863" height="500" alt="Screenshot 2026-03-25 145110" src="https://github.com/user-attachments/assets/eae47d7b-da3c-4696-bb64-f9c3594803fd" />
