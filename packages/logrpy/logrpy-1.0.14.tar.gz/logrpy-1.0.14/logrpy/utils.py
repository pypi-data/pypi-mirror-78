import os

def getcommit() -> str:
    try:
        return os.popen('git rev-parse HEAD').read().strip()
    except ValueError:
        return ''


def gettag() -> str:
    try:
        return os.popen('git tag -l --points-at HEAD').read().strip()
    except ValueError:
        return ''
