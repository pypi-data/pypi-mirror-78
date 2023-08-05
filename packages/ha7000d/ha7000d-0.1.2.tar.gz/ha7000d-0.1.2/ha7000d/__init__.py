"""HA7000D"""
import socket
from unyt import matplotlib_support, define_unit
from ha7000d.common import get_idn
from ha7000d.ha7062d import HA7062D

__all__ = ["CommChannel"]

define_unit("dBm", (1.0, "dB"))
define_unit("dBc", (1.0, "dB"))
matplotlib_support()
matplotlib_support.label_style = "/"

PORT = 9760


class CommChannel:
    """Connect to a HA7000D series phase noise analyzer

    Parameters
    ----------
        address (str): instrument's TCPIP address

    Returns
    -------
        CommChannel or HA7000D
    """

    def __init__(self, address):
        self._address = address
        self._sock = socket.create_connection((address, PORT))
        self._sock.settimeout(10)
        self._idn = get_idn(self._sock)
        manf = self._idn.manufacturer
        model = self._idn.model
        if not (manf.startswith("Holzworth") and model.startswith("HA7")):
            raise ValueError(f"Device at {address} is not a Holzworth HA7000D series")

    def __enter__(self):
        if self._idn.model == "HA7062D":
            return HA7062D(self._sock)
        raise NotImplementedError

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._sock.close()

    def get_instrument(self):
        """Return the HA7000D series instrument object"""
        return self.__enter__()

    def close(self):
        """Close the CommChannel"""
        self.__exit__(None, None, None)


def __dir__():
    return ["CommChannel", "__version__"]
