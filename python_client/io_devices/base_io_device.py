class BaseIODevice:
    def __init__(self, device_name):
        self.device_name = device_name
        self.status = {}


    def update(self):
        raise NotImplementedError("Subclasses should implement this method")

    def get_status(self):
        return self.status