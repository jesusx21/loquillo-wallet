from datetime import datetime
import re

from click import Context, ParamType
from click.core import Parameter


class DateType(ParamType):
    name = 'date'
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    def convert(self, value, param: Parameter | None, ctx: Context | None) -> datetime:
        if not isinstance(value, str) or self.pattern.fullmatch(value) is None:
            self.fail(f'{value} is not a valid date (expected YYYY-MM-DD)', param, ctx)

        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            self.fail(f'{value} is not a valid date (expected YYYY-MM-DD)', param, ctx)
