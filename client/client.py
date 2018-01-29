import pickle
import nacl.encoding
import nacl.signing
import datetime, socket

# Generate a new random signing key
signing_key = nacl.signing.SigningKey.generate()

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
print(update)

HOST, PORT = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(pickle.dumps(update))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
