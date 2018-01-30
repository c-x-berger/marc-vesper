# Class for the threaded TCP socketserver and associated additions
import socketserver
import socket
import pickle

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        self.database = None
        print("Loading pickled database...")
        with open("data.pickle", 'r+b') as db:
            try:
                self.database = pickle.load(db)
            except FileNotFoundError:
                print("No database file exists, loading empty DB.")
                open("data.pickle", 'w+') # create file
                self.database = {}
            except Exception as e:
                print(e)
                print("Error unpickling data!")
            finally:
                print("Finished loading {} from database.".format(self.database))
        self.address_family = socket.AF_INET6
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def setDB(self, data):
        self.database = data
    
    def server_close(self):
        print("Closing TCP server and saving database")
        super().server_close()
        with open("data.pickle", 'w+b') as db:
            pickle.dump(self.database, db)
