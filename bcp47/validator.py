
import re


class BCP47Validator(object):

    def __init__(self, bcp47):
        self.bcp47 = bcp47

    def validate_regex(self, lang_code):
        regex = r"^[a-zA-Z-]+$"
        if not re.match(regex, str(lang_code)):
            return "Invalid format"

    def validate(self, lang_code):
        if isinstance(lang_code, str):
            lang_code = self.bcp47.code_class(
                self.bcp47, lang_code.split('-'))
        regex_error = self.validate_regex(lang_code)
        if regex_error:
            return regex_error
        # parts = lang_code.split("-")
