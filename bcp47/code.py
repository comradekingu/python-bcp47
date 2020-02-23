

class BCP47Code(object):
    _errors = None
    _lang_code = None
    tag_parts = (
        "language",
        "extlang",
        "script",
        "region",
        "variant")

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
            errors = self.validate()
            if errors is None:
                self._errors = False
            self._errors = errors
        return self._errors

    @property
    def lang_code(self):
        return self._lang_code

    @property
    def extlang(self):
        return self.kwargs.get("extlang")

    @property
    def grandfather(self):
        return self.kwargs.get("grandfather")

    @property
    def language(self):
        return self.kwargs.get("language")

    @property
    def region(self):
        return self.kwargs.get("region")

    @property
    def script(self):
        return self.kwargs.get("script")

    @property
    def variant(self):
        return self.kwargs.get("variant")

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

    def _add_part(self, parts, part_type, name):
        if not name:
            return
        if part_type not in self.bcp47["%ss" % part_type]:
            raise Exception(
                "%s '%s' not recognized"
                % part_type.capitalize(), name)
        parts.append(name)

    def construct_from_kwargs(self, **kwargs):
        grandfather = kwargs.get("grandfather")
        language = kwargs.get("language")
        parts = []

        if grandfather and language:
            raise Exception(
                "You can only specify one of grandfather or language. "
                "You passed %s" % ((grandfather, language), ))
        if not (grandfather or language):
            raise Exception(
                "You must specify one of grandfather or language")
        for part in self.tag_parts:
            self._add_part(parts, part, kwargs.get(part))
        self.kwargs = kwargs
        self._errors = False
        self._lang_code = "-".join(parts)
