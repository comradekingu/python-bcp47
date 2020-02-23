
import re


class BCP47Validator(object):

    def __init__(self, parsed):
        self.parsed = parsed

    def validate_regex(self, lang_code):
        regex = r"^[a-zA-Z-]+$"
        if not re.match(regex, lang_code):
            return "Invalid format"

    def validate(self, lang_code):
        if not self.validate_regex(lang_code):
            return "Invalid format"
        # parts = lang_code.split("-")
