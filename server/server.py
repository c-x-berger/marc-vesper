from resource import Resource
from update import Update
import util
import database
import socketserver
import threading
import sys
import json
from threaded_tcp_server import ThreadedTCPServer

resources = database.Database()


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # I CAN HANDLE MYSELF OKAY
        self.data = self.request.recv(1024).strip()
        util.print_labeled(
            "Processing data from client {}".format(self.client_address[0]))
        util.print_labeled("Decoding binary -> string -> list...")
        decoded = None
        try:
            decoded = json.loads(self.data)
            print(decoded)
        except:
            util.print_labeled("BAD JSON! BAD! No decoding for you!")
            self.finish()
        util.print_labeled("recieved key {}".format(decoded[0]["key"]))
        util.print_labeled("Decoding complete. Processing...")
        self.as_update(decoded)

    def as_update(self, data):
        r, u = None, None
        resource_data = data[0]
        try:
            r = Resource(
                resource_data["label"], resource_data["serial_no"], resource_data["key"])
            u = Update(r, data[1], data[0]["value"], None)
        except KeyError:
            util.print_labeled(
                "Malformed dict from {}!".format(self.client_address[0]))
        # created resource and update objects, perform update
        try:
            u.oldres = resources.get()[resource_data["label"]]
        except KeyError:
            util.print_labeled("No old resource found for label {}".format(resource_data["label"]))
        util.print_labeled("Decoded JSON into update and resource")
        if (u.update_resource()):
            resources.setItem(resource_data["label"], r.toDict())
        self.finish()

    def finish(self):
        super().finish()
        exit()


def main(address, family):
    util.print_labeled("Starting socketserver")
    with ThreadedTCPServer((address, 9999), TCPHandler, True, family) as r_server:
        try:
            server_thread=threading.Thread(target=r_server.serve_forever)
            # Exit the server thread when the main thread terminates
            server_thread.daemon=True
            server_thread.start()
            resources.set(r_server.getDB())
            print("Server loop started in thread:", server_thread.name)
            while True:
                pass  # HACK for Ctrl+C interrupt
        except KeyboardInterrupt:
            print("\nCaught Ctrl+C")
            print("Shutting down...")
        finally:
            r_server.setDB(resources.get())
            r_server.shutdown()
            r_server.server_close()
            print(
                "Server thread terminated. Note that the socket may take some time to unbind.")
            exit(0)


def start():
    # server.start is more natural, this also allows us to make main() more complex
    util.print_labeled("Loading config...")
    from serverconfig import network_config
    main(network_config.address, network_config.family)


if __name__ == "__main__":
    start()
