# Class for the threaded TCP socketserver and associated additions
import socketserver
import socket
import pickle
import util


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        self.database = None
        print("Loading pickled database...")
        try:
            with open("data.pickle", 'r+b') as db:
                try:
                    self.setDB(pickle.load(db))
                except Exception as e:
                    print(e)
                    print("Error unpickling data!")
        except FileNotFoundError:
            util.print_labeled("No database file exists, loading empty DB.")
            self.setDB({})
            with open("data.pickle", 'w+b') as db:
                pickle.dump(self.database, db)
        finally:
            print("Finished loading {} from database.".format(self.database))
        self.address_family = socket.AF_INET6
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def setDB(self, data):
        self.database = data

    def getDB(self):
        return self.database

    def server_close(self):
        util.print_labeled("Closing TCP server and saving database")
        self.socket.close()
        with open("data.pickle", 'w+b') as db:
            pickle.dump(self.database, db)
