import pickle
import sys
import nacl.encoding
import nacl.signing
import datetime
import socket
import random
import getpass
import client_util


def randomBytes(n):
    return bytes(random.getrandbits(8) for i in range(n))


version = "0.0.1"


def main():
    print("marc_vesper client version {} starting...".format(version))
    # any real startup stuff can go here in the future
    host = input("Host: ")
    port = int(input("Port: "))
    family = None
    if (client_util.query_yes_no("IPv6?")):
        family = socket.AF_INET6
    else:
        family = socket.AF_INET
    print("Creating connection to {}/{}...".format(host, port))
    with socket.socket(family, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Connected to {}/{}!".format(host, port))
        # keygen
        pass_phrase = getpass.getpass(
            "Please enter your password for {}: ".format(host))
        random.seed(pass_phrase)
        signing_key = nacl.signing.SigningKey(
            randomBytes(32), nacl.encoding.RawEncoder)
        verify_key = signing_key.verify_key
        verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)
        print("(Re)generated signing key and verify key successfully!")
        # label, value, serial number
        label = input("Resource to update (label): ")
        value = input("Value to set resource to: ")
        current_time = datetime.datetime.now(datetime.timezone.utc)
        unix_time = current_time.timestamp()
        # update "object"
        update = [{"label": label, "serial_no": unix_time,
                   "key": verify_key_hex, "value": value}, None]
        pickled_update = pickle.dumps(update[0])
        # Sign a message with the signing key
        signed = signing_key.sign(pickled_update)
        update[1] = signed
        sock.sendall(pickle.dumps(update))


if __name__ == "__main__":
    main()
    exit(0)
