import sys
import socket
import threading
import logging

contador = 0

def make_tiny():
    logging.info(f'-- Increased request counter')
    global contador
    contador += 1
    return contador

def start(socket):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    try:
        while True:
            data = socket.recv(1024)
            logging.info(f'-- Recieving count notice')
            if not data:
                break
            request = str(make_tiny())
            #print("Peticiones : ", request)
            socket.sendall(request.encode('ascii'))

    except KeyboardInterrupt:
        #print("Cerrando servidor")
        socket.close()
        logging.info(f'KEYBOARD INTERRUPT SHUTDOWN')
    finally:
        socket.close()
        logging.info(f'TRANSACTION FINALIZATION')

def return_count_short():
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    try:
        while True:
            logging.info(f'-- Returning request count')
            data = socket.recv(1024)
            if not data:
                break
            request = str(make_tiny())
            #print("Peticiones : ",request)
            socket.sendall(request.encode('ascii'))

    except KeyboardInterrupt:
        #print("Cerrando servidor")
        socket.close()
        logging.info(f'KEYBOARD INTERRUPT SHUTDOWN')
    finally:
        socket.close()
        logging.info(f'TRANSACTION FINALIZATION')


def main():
    global THIS_HOST
    THIS_HOST = "ec2-54-226-49-19.compute-1.amazonaws.com"
    global THIS_PORT
    THIS_PORT = 3000
    print("Creating Socket")
    logging.info(f'TRANSACTION BEGINS')
    s = socket.socket()
    s.bind((THIS_HOST, THIS_PORT))
    try:
        s.listen(5)
        while True:
            conn, addr = s.accept()
            logging.info(f'-- Accept socket connection')
            #print("Connected to : ", addr)
            logging.info(f'CONNECTION ESTABLISHED IN {addr}')
            t = threading.Thread(target=start, args=(conn,))
            t.start()
            logging.info(f'-- Open thread')
    except KeyboardInterrupt:
        print("Error en main")
    finally:
        s.close()

if __name__ == "__main__":
    main()

    logging.basicConfig(filename="CountServer.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
