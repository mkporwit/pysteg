class StegoError(Exception):
    pass


class EncodeError(StegoError):
    def _init__(self, msg):
        self.msg = msg


class DecodeError(StegoError):
    def __init__(self, msg):
        self.msg = msg
