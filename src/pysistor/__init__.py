
class WrongParamException(Exception):
    pass


class InvalidImpException(Exception):
    pass


class PysistorFactory(object):
    backends = {}
    configs = {}

    def from_yaml(self, string, **kwargs):
        """ A convenience method for from_dict """
        pass

    def from_ini(self, string, prefix=None, **kwargs):
        """ A convenience method for from_dict """
        pass

    def from_yaml_str(self, string, **kwargs):
        """ A convenience method for from_dict """
        pass

    def from_ini_str(self, string, prefix=None, **kwargs):
        """ A convenience method for from_dict """
        pass

    def from_dict(self, **kwargs):
        """ Supply this function with a dictionary containing proper
        configuration information about a new backend and the backend will be
        initializaed """
        self._build_backend(kwargs)

    def _build_backend(self,
                       name=None,
                       backend="pysistor.backends.MemoryBackend",
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
