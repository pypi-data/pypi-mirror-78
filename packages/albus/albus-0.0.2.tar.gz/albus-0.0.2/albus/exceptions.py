# albus.exceptions


class AlbusError(Exception):

    def __init__(self, message, inner=None, detail=None):
        self.message = message
        self.inner = inner
        self.detail = detail
