

class BCP47Code(object):
    _errors = None
    _lang_code = None

    def __init__(self, bcp47, *args, **kwargs):
        self.bcp47 = bcp47
        self.construct(*args, **kwargs)

    def __repr__(self):
        return (
            "<%s.%s %s'%s' />"
            % (self.__module__,
               self.__class__.__name__,
               not self.valid and "INVALID ",
               self.lang_code))

    def __str__(self):
        return self.lang_code

    @property
    def errors(self):
        if self._errors is None:
            self._errors = self.validate()
        return self._errors

    @property
    def lang_code(self):
        return self._lang_code

    @property
    def valid(self):
        return not self.errors

    def validate(self):
        return self.bcp47.validate(self)

    def construct(self, *args, **kwargs):
        if args and kwargs:
            raise Exception(
                "Mixture of args and kwargs, "
                "use one or the other when constructing language codes")
        elif not (args or kwargs):
            raise Exception(
                "No arguments provided to construct a language code")
        if args:
            return self.construct_from_args(*args)
        return self.construct_from_kwargs(**kwargs)

    def construct_from_args(self, *args):
        return "-".join(args)

    def construct_from_kwargs(self, **kwargs):
        pass
