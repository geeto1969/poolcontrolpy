"""Exceptions for poolcontrolpy
"""


class HostError(Exception):
    """Raised when Pool Controller connection failed.

    Attributes
    ----------
    host : str
        Host name or IP address
    port : int
        Port number
    """

    def __init__(self, host: str, port: int):

        super().__init__()
        self.host = host
        self.port = port


class ResourceError(Exception):
    """Raised when API resource returns unexpected status"""

    def __init__(self, status: int, url: str):
        super().__init__()
        self.url = url
        self.status = status


class ResourceTypeError(Exception):
    """Raised when API resource returns unexpected type"""

    def __init__(self, url: str):
        super().__init__()
        self.url = url
