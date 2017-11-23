from os import environ as env, kill, getpid, remove
from os.path import exists


def get_tempdir():
    return env.get("TMPDIR") or\
        env.get("TEMPDIR") or\
        env.get("TMP") or\
        "/tmp"


class PidLock(object):
    def __init__(self, path):
        self.path = path

    def lock(self):
        if not self.unlock():
            return False
        with open(self.path, "w") as f:
            f.write(str(getpid()))
        return True

    def unlock(self):
        if exists(self.path):
            with open(self.path, "r") as f:
                pid = int(f.read())
                if pid and pid != getpid():
                    try:
                        kill(pid, 0)
                        return False
                    except OSError:
                        pass
            remove(self.path)
        return True
