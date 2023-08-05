import sys
import time
import json
import socket
import datetime
import traceback
from colorama import Fore, Style
from .logr import Logr
from .counter import Counter
from .levels import Weights, LevelDebug, LevelInfo, LevelNotice, LevelWarn, LevelError, LevelCrit, LevelAlert, LevelEmerg


class Logger:

    def __init__(self, config: Logr, logname: str, level: str = ''):
        self.config = config
        self.logname = logname
        self.conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.prefix = '{time} {level} '
        self.body = '[{version}, pid={pid}, {initiator}] {message}'
        self.level = level
        self.counter = Counter(config, logname)

    def getprefix(self, level: str) -> str:
        res = self.prefix
        res = res.replace('{time}', datetime.datetime.utcnow().isoformat())
        res = res.replace('{level}', Logger.colorlevel(level))
        return res

    def getbody(self, *args) -> str:
        msg = Logger.format(*args)
        res = self.body
        res = res.replace('{version}', self.config.getversion())
        res = res.replace('{pid}', str(self.config.pid))
        res = res.replace('{initiator}', Logger.initiator())
        res = res.replace('{message}', msg)
        return res

    def emerg(self, *args):
        self.log(LevelEmerg, *args)

    def alert(self, *args):
        self.log(LevelAlert, *args)

    def crit(self, *args):
        self.log(LevelCrit, *args)

    def error(self, *args):
        self.log(LevelError, *args)

    def warn(self, *args):
        self.log(LevelWarn, *args)

    def notice(self, *args):
        self.log(LevelNotice, *args)

    def info(self, *args):
        self.log(LevelInfo, *args)

    def debug(self, *args):
        self.log(LevelDebug, *args)

    def log(self, level: str, *args):
        prefix = self.getprefix(level)
        body = self.getbody(*args)
        files = {LevelEmerg: sys.stderr, LevelAlert: sys.stderr, LevelCrit: sys.stderr, LevelError: sys.stderr,
                 LevelWarn: sys.stdout, LevelNotice: sys.stdout, LevelInfo: sys.stdout, LevelDebug: sys.stdout}
        file = files.get(level, sys.stdout)
        print(prefix + body, file=file)
        self.send(level, body)

    def send(self, level: str, message: str):
        if Weights.get(level, -1) < Weights.get(self.level, -1):
            return
        payload = {
            'timestamp': str(time.time_ns()),
            'hostname': self.config.hostname,
            'logname': self.logname,
            'level': level,
            'pid': self.config.pid,
            'version': self.config.getversion(),
            'message': message
        }
        cipher_log = self.config.cipher.encrypt(json.dumps(payload))
        pack = {
            'public_key': self.config.public_key,
            'cipher_log': cipher_log
        }
        self.conn.sendto(json.dumps(pack).encode(), self.config.udp)

    @staticmethod
    def format(*args) -> str:
        template = ''
        for _ in range(len(args)):
            template += '{} '
        return template.format(*args)

    @staticmethod
    def initiator() -> str:
        stack = traceback.format_stack()[-5]
        splitted = stack.split('"')
        name = splitted[1]
        line = splitted[2].split(',')[1][6:]
        return name + ':' + line

    @staticmethod
    def colorlevel(level: str) -> str:
        styles = {LevelDebug: Fore.BLUE, LevelInfo: Fore.GREEN, LevelNotice: Fore.GREEN + Style.BRIGHT,
                  LevelWarn: Fore.YELLOW, LevelError: Fore.LIGHTRED_EX, LevelCrit: Fore.RED,
                  LevelAlert: Fore.RED + Style.BRIGHT, LevelEmerg: Fore.RED + Style.BRIGHT}

        style = styles.get(level, Style.BRIGHT)

        return style + level + Style.RESET_ALL
