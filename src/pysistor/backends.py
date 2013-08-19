import datetime

class MemoryBackend(object):

    def __init__(self):
        self.store = {}

    def store(self, key, value, expire=None):
        if expire is not None:
            if not isinstance(expire, datetime.datetime):
                except AttributeError("Expiry time must be a datetime object")
        self.store[key] = (value, expire)

    def expire(self, key):
        del self.store[key]

    def __getattr__(self, key:qa


