import resource
import update
import pickle
import socketserver, threading

resources = {}

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # I CAN HANDLE MYSELF OKAY
        self.data = self.request.recv(1024).strip()
        print("Processing data from client {} in thread {}".format(
                self.client_address[0],
                threading.current_thread().name
            )
        )
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
        resources[decoded[0]["label"]] = r.toDict()

def main():
    print("Starting socketserver")
    with ThreadedTCPServer(("localhost", 9999), TCPHandler) as r_server:
        try:
            server_thread = threading.Thread(target=r_server.serve_forever)
            # Exit the server thread when the main thread terminates
            # server_thread.daemon = True
            server_thread.start()
            print("Server loop running in thread:", server_thread.name)
            while True:
                pass # HACK for Ctrl+C interrupt
        except KeyboardInterrupt:
            print("\nCaught Ctrl+C")
            print("Shutting down...")
            r_server.shutdown()
