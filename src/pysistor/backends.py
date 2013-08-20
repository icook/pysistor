import datetime

class MemoryBackend(object):
    """ The memeory backend acts as a class suitible for testing or very simple
    uses. Not intended for production use. In theory it should work for single
    process executions. """

    def store(self, key, value, expire=None):
        if expire is not None:
            if not isinstance(expire, datetime.datetime):
                raise AttributeError("Expiry time must be a datetime object")
        self.__dict__[key] = (value, expire)

    def expire(self, key):
        del self.__dict__[key]

    def get(self, key):
        self[key]

    def __getitem__(self, key):
        val = self.__dict__[key]
        # Check if data has expired or has an expiry at all
        if val[1] is not None and val[1] < datetime.datetime.now():
            self.expire(key)
            return

        return val[0]
