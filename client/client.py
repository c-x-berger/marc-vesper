import pickle
import nacl.encoding
import nacl.signing
import datetime

# Generate a new random signing key
signing_key = nacl.signing.SigningKey.generate()

# Obtain the verify key for a given signing key
verify_key = signing_key.verify_key

# Serialize the verify key to send it to a third party
verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)

current_time = datetime.datetime.now(datetime.timezone.utc)
unix_time = current_time.timestamp()
update = [{"label": "test.hype", "serial_no": unix_time, "key": verify_key_hex}, None]

pickled_update = pickle.dumps(update[0])

# Sign a message with the signing key
signed = signing_key.sign(pickled_update)
update[1] = signed
