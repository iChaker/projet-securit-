from cryptography import x509 
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from hashlib import sha3_512
import time
key = rsa.generate_private_key( public_exponent=45451,
                                key_size=2048,
                                backend=default_backend()
 )

with open("CAkey.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b'qQb'),
    ))
    
time.sleep(3)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
with open("CAkey.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=b'qQb',
        backend=default_backend()
    )