import os
import socket
import hashlib
import base64
from .aes import AESCipher
from .utils import getcommit, gettag

commit = getcommit()
tag = gettag()
pid = os.getpid()


class Logr:

    def __init__(self, udp: tuple, public_key: str, private_key: str, hostname: str = '', version: str = ''):
        key_bytes = base64.b64decode(private_key)
        self.udp = udp
        self.public_key = public_key
        self.private_hash = hashlib.sha256(key_bytes).digest()
        self.cipher = AESCipher(self.private_hash)
        self.hostname = hostname or socket.gethostname()
        self.version = version
        self.pid = pid

    def getversion(self) -> str:
        if self.version:
            return self.version
        elif tag != '':
            return tag
        elif len(commit) >= 6:
            return commit[0: 6]
        else:
            return ''

    def getlogger(self, logname: str, **opts):
        from .logger import Logger
        return Logger(self, logname, **opts)

    def getcounter(self, *args):
        from .counter import Counter
        return Counter(self, *args)
