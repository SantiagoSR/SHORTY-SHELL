import socket
import cmd
import logging
import pyqrcode
import struct

def create_socket(HOST, PORT):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    logging.info(f'-- Created socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def shorten(url):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s", 
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )    
    logging.info(f'STARTED SHORTENING TRANSACTION FOR URL:{url}')
    global SHORT_HOST
    SHORT_HOST = "ec2-54-227-29-29.compute-1.amazonaws.com"
    global SHORT_PORT
    SHORT_PORT = 3000
    s = create_socket(SHORT_HOST, SHORT_PORT)
    s.send(url.encode('ascii'))
    logging.info(f'-- Sent URL')
    new_url = s.recv(1024).decode()
    logging.info(f'-- Received QR')
    print(f"{new_url}")

def get_requests():
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s", 
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    logging.info(f'STARTED GET REQUESTS TRANSACTIONS')
    global COUNT_HOST
    COUNT_HOST = "ec2-54-226-49-19.compute-1.amazonaws.com"
    global COUNT_PORT 
    COUNT_PORT = 3000
    s = create_socket(COUNT_HOST, COUNT_PORT)
    wanted = "How many?"
    s.send(wanted.encode('ascii'))
    logging.info(f'-- Sent request')
    short_requests = s.recv(1024).decode()
    logging.info(f'-- Received Amount')
    print(f"{short_requests}")

def QR(url):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s", 
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    logging.info(f'STARTED QR GENERATION TRANSACTION FOR URL:{url}')
    global QR_HOST
    QR_HOST = "ec2-3-229-116-214.compute-1.amazonaws.com"
    global QR_PORT
    QR_PORT = 3000
    s = create_socket(QR_HOST, QR_PORT)
    s.send(url.encode('ascii'))
    logging.info(f'-- Sent URL')
    qr_code = s.recv(65536).decode()
    logging.info(f'-- Received QR')
    print(f"{qr_code}")
    #s.close()

def STATUS(url):
    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s", 
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    logging.info(f'STARTED STATUS GENERATION TRANSACTION FOR URL:{url}')
    global STATUS_HOST
    STATUS_HOST = "ec2-44-198-32-98.compute-1.amazonaws.com"
    global STATUS_PORT
    STATUS_PORT = 3000
    s = create_socket(STATUS_HOST, STATUS_PORT)
    s.send(url.encode('ascii'))
    logging.info(f'-- Sent URL')
    STATUS_code = s.recv(104000).decode()
    logging.info(f'-- Received STATUS')
    print(f"{STATUS_code}")

class ShortyShell(cmd.Cmd):
    intro = "Welcome to shorty, the URL shortner. \n Type help COMMAND_NAME to see further information about the command. \n Type bye to leave."
    prompt = "ShortyShell -> "
    file = None

    def do_SHORT(self, arg):
        'Shortens a given URL: SHORT <URL>'
        shorten(str(arg))
    def do_STATUS(self, arg):
        'GEnerates STATUS based on URL: STATUS <URL> '
        STATUS(str(arg))
    def do_REQUESTS(self, arg):
        'Returns the amount of requests our servers have attended: REQUESTS'
        get_requests()
    def do_QR(self, arg):
        'Returns the amount of requests our servers have attended: QR <URL>'
        QR(str(arg))
    def do_bye(self, arg):
        'Stop recording, close the turtle window, and exit:  BYE'
        print('Bye bye!')
        self.close()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

def main():
    shell = ShortyShell()

    try:
        shell.cmdloop()
    except Exception as e:
        print(f"Sorry, we were not expecting that. {e}")

if __name__ == "__main__":
    main()

    logging.basicConfig(filename="Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )
