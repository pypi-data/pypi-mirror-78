import threading
import psutil
import socket
import json
from .logr import Logr
from .count import Count


class Counter:

    def __init__(self, config: Logr, logname: str):
        self.config = config
        self.logname = logname
        self.conn = None
        self.tmp = {}
        self.timer = None
        self.system = False

    def connect(self):
        if self.conn is None:
            self.conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def run(self, interval: int):
        if self.timer is None:
            self.timer = threading.Timer(interval, self.flush)
            self.timer.start()

    def flush(self):
        if self.system:
            la = psutil.getloadavg()
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            self.per('la', la[0], 100)
            self.per('cpu', cpu, 100)
            self.per('ram', ram.percent, 100)
            self.per('disk', disk.percent, 100)
        tmp = self.tmp
        self.tmp = {}
        for key in tmp:
            value = tmp.get(key)
            self.send(value)

    def stop(self):
        self.flush()

    def send(self, data: Count):
        cipher_count = self.config.cipher.encrypt(data.tojson())
        pack = {
            'public_key': self.config.public_key,
            'cipher_count': cipher_count
        }
        self.conn.sendto(json.dumps(pack).encode(), self.config.udp)

    def blank(self):
        return {
            'hostname': self.config.hostname,
            'logname': self.logname,
            'version': self.config.getversion(),
        }

    def touch(self, keyname: str) -> Count:
        self.connect()
        self.run(20)
        if self.tmp.get(keyname) is None:
            count = Count({'keyname': keyname, **self.blank()})
            self.tmp[keyname] = count
        return self.tmp[keyname]

    def inc(self, key: str, num: float = 1):
        return self.touch(key).inc(num)

    def max(self, key: str, num: float):
        return self.touch(key).max(num)

    def min(self, key: str, num: float):
        return self.touch(key).min(num)

    def avg(self, key: str, num: float):
        return self.touch(key).avg(num)

    def per(self, key: str, taken: float, total: float):
        return self.touch(key).per(taken, total)

    def time(self, key: str, duration: int):
        return self.touch(key).time(duration)

    def snippet(self, kind: str, keyname: str, limit: int = 30):
        return json.dumps({
            'widget': 'counter',
            'kind': kind,
            'keyname': keyname,
            'limit': limit,
            **self.blank()
        })

    def watchsystem(self):
        self.system = True
