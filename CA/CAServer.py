from cryptography.hazmat.primitives.serialization import load_ssh_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import socket
import os
import gc
import functools


def key_decorator(func):
    def key_check(*args, **kwargs):
        if args[0].private_key == None:
            print("Use load_private_key before using this method. Don't forget to unload the key afterwards")
            return False
        else:
            return func(*args, **kwargs)
    return key_check
class CAServer():

        

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, port))
        self.private_key = None

    def load_private_key(self,path="CAkey.pem",password=b'qQb'):
        if os.path.isfile(path):
            try:
                with open(path, "rb") as key_file:
                    self.private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=password,
                        backend=default_backend()
                    )
                    print("Key loaded from disk")

            except:
                print("Wrong Password")
        else:
            print("Wrong Path")
    
    def unload_private_key(self,path):
        self.private_key = None
        gc.collect()

    @key_decorator
    def sign(self,message):
        signed_message = self.private_key.sign(
                                        message,
                                        padding.PSS(
                                        mgf=padding.MGF1(hashes.SHA256()),
                                        salt_length=padding.PSS.MAX_LENGTH),
                                        hashes.SHA256())
        return signed_message
        
    @key_decorator
    def verify(self,message):

        pem = self.private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1
        )

        self.private_key.public_key().verify(
            message,
            pem,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    @key_decorator
    def decrypt(self,message):
        pass


if __name__ == "__main__":
    sv = CAServer("127.0.0.1",80)
    sv.load_private_key()
    signed = sv.sign(b'ASBA')
    help(sv.private_key.public_key().verify)
    sv.verify(signed)



            
