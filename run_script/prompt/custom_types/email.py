from click import ParamType
import re


class EmailType(ParamType):
    name = 'email'

    def convert(self, value, param, ctx):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(pattern, value):
            self.fail(f"{value} is not a valid email address", param, ctx)

        return value
