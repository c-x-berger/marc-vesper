import threading
import util


class Database(object):
    def __init__(self, initial={}):
        self.data = initial
        self.lock = threading.Lock()

    def set(self, d):
        with self.lock:
            self.data = d

    def get(self):
        with self.lock:
            return self.data

    def setItem(self, key, data):
        with self.lock:
            self.data[key] = data
            print(self.data)

    def getItem(self, key):
        with self.lock:
            return self.data[key]
