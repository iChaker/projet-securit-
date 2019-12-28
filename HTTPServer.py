from argparse import ArgumentParser
from ipaddress import IPv4Address
from subprocess import Popen           
import threading
import socket
import os
__version__ = "0.0.1"

class ChatServer(threading.Thread):
    
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {} 
        
        try:
            self.server.bind((self.host, self.port))
            print("SERVER SUCCESSFULLY BINDED")
        except socket.error:
            print('Bind failed %s' % (socket.error))

        self.server.listen(10)
        
    # Not currently used. Ensure sockets are closed on disconnect
    def exit(self):
        self.server.close()

    def run_thread(self, conn, addr):
        print('Client connected with ' + addr[0] + ':' + str(addr[1]))
        while True:
            data = conn.recv(1024)
            reply = b'OK...' + data
            print(reply)
            conn.sendall(reply) 
        	
        conn.close() # Close

    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        # We need to run a loop and create a new thread for each connection
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.run_thread, args=(conn, addr)).start()

if __name__ == "__main__":

    parser = ArgumentParser(usage="hostIP, port", description="simple async HTTP server")
    parser.add_argument("hostIP",type=str)
    parser.add_argument("port",type=int)

    args = parser.parse_args()
    try:
        hostip = str(IPv4Address(args.hostIP))
        port = args.port
    except:
        print("Bad parameters")
    os.system("python ")
    sv = ChatServer(hostip,port)
    
    sv.run()

    input("press enter to close server")





