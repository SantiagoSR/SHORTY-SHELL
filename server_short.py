#!/usr/bin/env python3

from __future__ import with_statement														
import sys
import socket
import threading
import contextlib
import logging

try:
	from urllib.parse import urlencode		

except ImportError:
	from urllib import urlencode

try:
	from urllib.request import urlopen

except ImportError:
	from urllib.request import urlopen

def make_tiny(url):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    
    with contextlib.closing(urlopen(request_url)) as response:
        logging.info(f'-- Shortened URL')
        return response.read().decode('utf-8')

def create_socket(HOST, PORT):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    logging.info(f'-- Established socked connection')
    return s

def llamada_servidor_contar():
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    try: 
        global COUNT_HOST 
        COUNT_HOST = "ec2-54-226-49-19.compute-1.amazonaws.com"
        global COUNT_PORT 
        COUNT_PORT = 3000
        #s.connect((HOST, PORT))
        s = create_socket(COUNT_HOST, COUNT_PORT)
        message = "Pedir numero de peticiones que llevamos"
        s.send(message.encode('ascii'))
        logging.info(f'-- Sent count request')
        #print("Numero de peticiones resueltas")
        #s.recv(1024).decode()
    except Exception as e:
        #print(f"Connection with server 1 error by {e}")
        logging.info(f'FINISHED BY EXCEPTION {e}')

def start(socket):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    try:
        llamada_servidor_contar()
        logging.info(f'-- Calls on COUNT_SERVER')
        while True:
            data = socket.recv(1024)
            logging.info(f'-- Received URL to shorten')
            if not data:
                break
            url = data.decode()
            request = make_tiny(url)
            logging.info(f'-- SHORTENED URL')
            socket.sendall(request.encode('ascii'))
            logging.info(f'-- Returned shortened URL')
    
    except KeyboardInterrupt:
        print("Cerrando servidor")
        socket.close()
    finally:
        socket.close()

def main():
    print("Creating Socket")
    s = socket.socket()
    global THIS_HOST
    THIS_HOST = "127.0.0.1"
    global THIS_PORT 
    THIS_PORT = 3003
    s.bind((THIS_HOST, THIS_PORT))
    try:
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print("Connected to : ", addr)
            t = threading.Thread(target=start, args=(conn,))
            t.start()
    except KeyboardInterrupt:
        print("Error en main")
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
