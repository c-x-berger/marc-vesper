import json
import sys
import nacl.encoding
import nacl.signing
import datetime
import socket
import random
import time
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
        verify_key_b64 = str(verify_key.encode(
            encoder=nacl.encoding.URLSafeBase64Encoder), "utf-8")
        print("(Re)generated signing key and verify key successfully!")
        # label, value, serial number
        r_type = int(input("Type of request: "))
        label = input("Label: ")
        if (r_type == 100):
            value = input("Value to set resource to: ")
            current_time = datetime.datetime.now(datetime.timezone.utc)
            unix_time = current_time.timestamp()
            # update "object"
            update = [{"label": label, "serial_no": unix_time,
                       "key": verify_key_b64, "value": value}, None, 100]
            json_update = json.dumps(update[0])
            # Sign a message with the signing key
            signed = str(signing_key.sign(bytes(json_update, "utf-8"),
                                          nacl.encoding.URLSafeBase64Encoder), "utf-8")
            update[1] = signed
            print(json.dumps(update))
            sock.sendall(bytes(json.dumps(update), "utf-8"))
        elif (r_type == 200):
            data = [label, "EMPTY", 200]
            json_request = json.dumps(data)
            print(json_request)
            sock.sendall(bytes(json_request, "utf-8"))
            print(str(sock.recv(1024), "utf-8"))


if __name__ == "__main__":
    main()
    exit(0)
