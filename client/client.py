import pickle
import sys
import nacl.encoding
import nacl.signing
import datetime, socket, random

def randomBytes(n):
    return bytes(random.getrandbits(8) for i in range(n))

# Generate a new random signing key
random.seed(sys.argv[2])
signing_key = nacl.signing.SigningKey(randomBytes(32), nacl.encoding.RawEncoder)

# Obtain the verify key for a given signing key
verify_key = signing_key.verify_key

# Serialize the verify key to send it to a third party
verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)

current_time = datetime.datetime.now(datetime.timezone.utc)
unix_time = current_time.timestamp()
update = [{"label": "test.hype", "serial_no": unix_time, "key": verify_key_hex, "value": "fcc3:a9d9:1694:2d:7a61:b5af:95fb:85d6"}, None]

pickled_update = pickle.dumps(update[0])

# Sign a message with the signing key
signed = signing_key.sign(pickled_update)
update[1] = signed

HOST = str(sys.argv[1])
print("HOST: {}".format(HOST))
PORT = 9999

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(pickle.dumps(update))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
