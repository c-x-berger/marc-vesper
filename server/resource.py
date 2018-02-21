class Resource():
    def __init__(self, label, serial_no, key):
        self.label = label
        self.serial_no = serial_no
        self.key = key
        self.value = None

    def toDict(self):
        return {"key": self.key, "value": self.value, "serial_no": self.serial_no}
