import nacl.signing
import pickle
import util


class Update():
    def __init__(self, resource, signature, value, oldres=None):
        self.resource = resource
        self.sig = signature
        self.value = value
        self.oldres = oldres

    def check_sig(self):
        sig_key_recv = nacl.signing.VerifyKey(
            self.resource.key, encoder=nacl.encoding.HexEncoder)
        try:
            util.print_labeled("Verifying data...")
            sig_key_recv.verify(self.sig)
            if (self.oldres != None):
                util.print_labeled(
                    "Signature good for RECIEVED key, checking against SERVER key")
                sig_key_serv = nacl.signing.VerifyKey(
                    self.oldres["key"], encoder=nacl.encoding.HexEncoder)
                util.print_labeled(str(self.oldres["key"], "utf-8"))
                sig_key_serv.verify(self.sig)
            return True
        except nacl.exceptions.BadSignatureError:
            util.print_labeled("Bad signature!")
            return False

    def update_resource(self):
        if (self.check_sig()):
            # signature checks out
            # value should be an IPv6 address
            util.print_labeled("Signature checks out, updating resource.")
            self.resource.value = self.value
            return True
        else:
            # it doesn't
            util.print_labeled(
                "Passing due to signature error. No values have been updated.")
            return False
