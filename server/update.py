import nacl.signing
import pickle

class Update():
    def __init__(self, resource, signature, value):
        self.resource = resource
        self.sig = signature
        self.value = value

    def check_sig(self):
        sig_key = nacl.signing.VerifyKey(self.resource.key, encoder=nacl.encoding.HexEncoder)
        try:
            print("Trying to verify signature...")
            sig_key.verify(self.sig)
            return True
        except nacl.exceptions.BadSignatureError:
            print("Bad signature!")
            return False

    def update_resource(self):
        if (self.check_sig()):
            # signature checks out
            # value should be an IPv6 address
            self.resource.value = self.value
        else:
            # it doesn't
            print("Passing due to signature error. No values have been updated.")
            pass
