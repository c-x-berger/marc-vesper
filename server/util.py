import threading

def print_labeled(data):
    print(("[{}] " + data).format(threading.current_thread().name))
