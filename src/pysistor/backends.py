import datetime

class MemoryBackend(object):
    """ The memeory backend acts as a class suitible for testing or very simple
    uses. Not intended for production use. In theory it should work for single
    process executions. """

    def __init__(self):
        self.store = {}

    def store(self, key, value, expire=None):
        if expire is not None:
            if not isinstance(expire, datetime.datetime):
                except AttributeError("Expiry time must be a datetime object")
        self.store[key] = (value, expire)

    def expire(self, key):
        del self.store[key]

    def get(self, key):
        self.__getattr__(key)

    def __getattr__(self, key):
        val = self.__dict__[key]

        # Check if data has expired or has an expiry at all
        if val[0] and val[0] < datetime.datetime.now():
            self.expire(key)
            return

        return val[1]


