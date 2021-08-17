#!/usr/bin/env python3

import sys
import socket
import threading
import contextlib
import pyqrcode
import struct
import logging

def make_qr(url):

    qr = pyqrcode.create(url).terminal()
    return qr

def create_socket(HOST, PORT):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    logging.info(f'CREATED SOCKET')
    return s

def llamada_servidor_short(url):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    logging.info(f'Started shortening transaction for URL:{url}')
    global SHORT_HOST
    SHORT_HOST = "ec2-54-227-29-29.compute-1.amazonaws.com"
    global SHORT_PORT
    SHORT_PORT = 3003
    s = create_socket(SHORT_HOST, SHORT_PORT)
    s.send(url.encode('ascii'))
    logging.info(f'-- Sent URL')
    new_url = s.recv(1024).decode()
    logging.info(f'-- Received QR')
    return new_url

def start(socket):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    try:
        while True:
            data = socket.recv(1048)
            logging.info(f'-- Receiving data')
            if not data:
                break
            url = llamada_servidor_short(data.decode())
            logging.info(f'-- Calling shorty server')
            #print(url)
            request = make_qr(url)
            socket.sendall(request.encode('ascii'))
            logging.info(f'-- Sending back QR')
    
    except KeyboardInterrupt:
        #print("Cerrando servidor")
        logging.info(f'TRANSACTION ENDED BY KEYBOARD INTERRUPT')
        socket.close()
    finally:
        logging.info(f'TRANSACTION ENDED')
        socket.close()

def main():
    print("Creating Socket")
    s = socket.socket()
    global THIS_HOST 
    THIS_HOST = "127.0.0.1"
    global THIS_PORT
    THIS_PORT = 3000
    s.bind((THIS_HOST, THIS_PORT))
    try:
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print("Connected to : ", addr)
            t = threading.Thread(target=start, args=(conn,))
            t.start()
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
    
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )

