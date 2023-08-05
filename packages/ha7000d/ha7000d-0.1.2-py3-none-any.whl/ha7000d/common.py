"""Common definitions"""
from collections import namedtuple

IDN = namedtuple("IDN", ["manufacturer", "model", "serial_number", "firmware_version"])


def get_idn(sock):
    """Get IDN"""
    sock.send(bytes(":IDN?\n", "utf-8"))
    idn = []
    for val in sock.recv(500).decode("utf-8").strip("\n").split(","):
        if val.startswith("Ver"):
            idn.append(val.split(":")[-1])
        idn.append(val.strip())
    return IDN(*idn)


class HA7000DBase:
    """Instrument base class

    Parameters
    ----------
        sock : `~socket.socket`
    """

    def __init__(self, sock):
        self._sock = sock
        self._idn = get_idn(sock)

    def __setattr__(self, name, value):
        if hasattr(self, name) and isinstance(getattr(self, name), HA7000DBase):
            raise AttributeError(f"can't set '{name}'")
        if hasattr(self.__class__, name):
            prop = getattr(self.__class__, name)
            try:
                prop.fset(self, value)
            except TypeError:
                raise AttributeError(f"can't set '{name}'") from None
        else:
            self.__dict__[name] = value

    def __repr__(self):
        raise NotImplementedError

    def __dir__(self):
        inst_attr = list(filter(lambda k: not k.startswith("_"), self.__dict__.keys()))
        cls_attr = list(filter(lambda k: not k.startswith("_"), dir(self.__class__)))
        return inst_attr + cls_attr

    def _write(self, cmd):
        cmd = bytes(f"{cmd}\n", "utf-8")
        self._sock.send(cmd)

    def _read(self, buffer=1000):
        resp = ""
        while True:
            resp += self._sock.recv(buffer).decode("utf-8")
            if resp[-1] == "\n":
                break
        return resp.strip()

    def _query(self, cmd):
        self._write(cmd)
        return self._read()

    def _set_parameter(self, cmd):
        self._write(cmd)
        return self._read()

    def reset(self):
        """Reset to factory default"""
        return self._write("*RST")


class Subsystem(HA7000DBase):
    """Base class for a specific measurement function

    Attributes:
        instr (HA7000D)
    """

    _kind = "Instrument"

    def __init__(self, instr):
        super().__init__(instr._sock)
        self._instr = instr

    def __init_subclass__(cls, kind):
        cls._kind = kind

    def __get__(self, instance, owner=None):
        return self

    def __repr__(self):
        return f"<{self._instr.model} {self._kind}>"
