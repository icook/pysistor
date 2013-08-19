class WrongParamException(Exception):
    pass


class InvalidImpException(Exception):
    pass


class PysistorFactory(object):
    backends = {}
    configs = {}
    default = None

    @classmethod
    def from_yaml(cls, string, **kwargs):
        """ A convenience method for from_dict """
        pass

    @classmethod
    def from_ini(cls, string, prefix=None, **kwargs):
        """ A convenience method for from_dict """
        pass

    @classmethod
    def from_yaml_str(cls, string, **kwargs):
        """ A convenience method for from_dict """
        pass

    @classmethod
    def from_ini_str(cls, string, prefix=None, **kwargs):
        """ A convenience method for from_dict """
        pass

    @classmethod
    def from_dict(cls, **kwargs):
        """ Supply this function with a dictionary containing proper
        configuration information about a new backend and the backend will be
        initializaed """
        cls._build_backend(kwargs)

    def _build_backend(self,
                       name=None,
                       backend="pysistor.backends.MemoryBackend",
                       set_default=False,
                       **kwargs):
        """ Internally takes a configuration dictionary and builds a backend """
        parts = backend.split('.')
        backend_mod = parts[0:-1].join('.')
        backend_class = parts[-1]

        # Set a default name
        if name is None:
            name = backend_class

        # Make sure we don't start building a duplicated name
        if name in backends:
            raise AttributeError("There is already a backend with that name")


        try:
            module = __import__(backend_mod, fromlist=[backend_class])
        except ImportError:
            raise ImportError("Dotted path {0} given for your backend could not"
                              " be imported!")

        backend_cls = getattr(module, backend_class, None)

        # Do our class checks
        for func in ['add_key', 'expire_key']:
            if not callable(getattr(backend_cls, func)):
                raise InvalidImpException("Backend must implement correct "
                                          "methods")

        # Should raise a WrongParamException if caller didn't include valid
        # config
        inst = backend_cls(**kwargs)
        # Add to internal dict
        backends[name] = inst

        # setup our default if requested
        if set_default:
            self.default = inst

    def __getitem__(self, key):
        if key is None:
            return self.default

        try:
            return self.backends[key]
        except KeyError:
            raise KeyError("Requested backend '{0}' doesn't exist".format(key))

class BaseAdapter(object):
    """ This should be used as a base for other framework adapters. Empty method
    implementation provide guidelines for implementation of subclasses. Adapters
    provide are the primary exposed interface to users. """

    def store(self, key, value, expire=None, backend=None):
        """ Allow user to store data in a specific backend, or the default
        backend if ommitted. The default implementation makes the assumption
        that factory is an accessible attribute. """
        self.factory[backend].store(key, value, expire)

    def expire(self, key, backend=None):
        """ Allow user to remove data in a specific backend, or the default
        backend if ommitted. The default implementation makes the assumption
        that factory is an accessible attribute. """
        self.factory[backend].expire(key)

    def get(self, key, backend=None):
        """ Allow user to access data in a specific backend, or the default
        backend if ommitted. The default implementation makes the assumption
        that factory is an accessible attribute. """
        self.factory[backend][key]

    @property
    def factory(self):
        """ This method should provide a getter method to access the
        PysistorFactory in a way compatible with the adapter framework.
        PyramidAdapter provides a canonical example by storing it in the registry. """
        pass

    def setup(self):
        """ Method should do neccessary setup to persist the Factory for access
        later. This is intended to be a helper method to be run at
        configuration time for your framework. """
        pass



class PyramidAdapter(BaseAdapter):

    def __init__(self, request):
        self.request = request

    @property
    def factory(self):
        return getattr(self.request.registry, '_pysistor_factory', None)

    @factory.setter
    def factory(self, new_factory):
        self.request.registry._pysistor_factory = new_factory

    @classmethod
    def setup(cls, factory, regitry):
        registry._pysistor_factory = factory
