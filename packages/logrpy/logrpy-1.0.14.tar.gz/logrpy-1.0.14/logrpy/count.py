import json
import time


class Count:

    def __init__(self, data: dict):
        for key in data:
            setattr(self, key, data[key])
        self.metrics = {}
        self.now()

    def tojson(self) -> str:
        return json.dumps(self.__dict__)

    def now(self):
        self.timestamp = int(time.time())

    def inc(self, num: float = 1):
        self.now()
        if self.metrics.get('inc') is None:
            self.metrics['inc'] = 0
        self.metrics['inc'] += num
        return self

    def max(self, num: float):
        self.now()
        if self.metrics.get('max') is None:
            self.metrics['max'] = num
        else:
            self.metrics['max'] = max(self.metrics['max'], num)
        return self

    def min(self, num: float):
        self.now()
        if self.metrics.get('min') is None:
            self.metrics['min'] = num
        else:
            self.metrics['min'] = min(self.metrics['min'], num)
        return self

    def avg(self, num: float):
        self.now()
        if self.metrics.get('avg_num') is None:
            self.metrics['avg_sum'] = 0
            self.metrics['avg_num'] = 0
        self.metrics['avg_sum'] += num
        self.metrics['avg_num'] += 1
        return self

    def per(self, taken: float, total: float = 0):
        self.now()
        if self.metrics.get('per_ttl') is None:
            self.metrics['per_tkn'] = 0
            self.metrics['per_ttl'] = 0
        self.metrics['per_tkn'] += taken
        self.metrics['per_ttl'] += total
        return self

    def time(self, duration: int = 1e6):
        self.now()
        self.metrics['time'] = duration
        ts = time.time_ns()
        delta = None

        def calc():
            nonlocal delta
            if delta is not None:
                return delta
            delta = time.time_ns() - ts
            self.avg(delta).max(delta).min(delta)
            return delta

        return calc
