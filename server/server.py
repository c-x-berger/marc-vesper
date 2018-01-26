import resource
import update
import pickle
import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # I CAN HANDLE MYSELF OKAY
        self.data = self.request.recv(1024).strip()
        print("Processing data from client {}".format(self.client_address[0]))
        decoded = pickle.loads(self.data)
        print(decoded)
        r, u = None, None
        try:
            r = resource.Resource(decoded[0]["label"], decoded[0]["serial_no"], decoded[0]["key"], None)
            u = update.Update(r, decoded[1], decoded[0]["value"])
        except KeyError:
            # recieved malformed dict
            print("Malformed dict from {}!".format(self.client_address[0]))
        print("Decoded pickle into update object and resource object")

def main():
    print("Starting socketserver")
    with socketserver.TCPServer(("localhost", 9999), TCPHandler) as r_server:
        r_server.serve_forever()
    r_server.shutdown()
