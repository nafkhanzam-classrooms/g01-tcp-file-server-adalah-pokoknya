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
### Client.py
### Server-thread.py
### Server-sync.py
### Server-select.py
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


### Server-poll.py

## Screenshot Hasil
### 1. Server thread
<img width="1864" height="474" alt="Screenshot 2026-03-25 144434" src="https://github.com/user-attachments/assets/8394fbb0-8442-4957-922f-f30d8ab99027" />

### 2. Server sync
<img width="1864" height="489" alt="Screenshot 2026-03-25 144737" src="https://github.com/user-attachments/assets/6bc39e8f-aef9-462c-b2db-b63de4f713f7" />

### 3. Server select
<img width="1919" height="571" alt="Screenshot 2026-03-25 144939" src="https://github.com/user-attachments/assets/e4ade567-539c-40a2-af12-89c41e7e1382" />

### 4. Server poll
<img width="1863" height="500" alt="Screenshot 2026-03-25 145110" src="https://github.com/user-attachments/assets/eae47d7b-da3c-4696-bb64-f9c3594803fd" />
