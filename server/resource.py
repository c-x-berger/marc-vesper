class Resource():
    def __init__(self, label, serial_no, key, value):
        self.label = label
        self.serial_no = serial_no
        self.key = key
        self.value = value

    def toDict(self):
        return {"key": self.key, "value": self.value, "serial_no": self.serial_no}

