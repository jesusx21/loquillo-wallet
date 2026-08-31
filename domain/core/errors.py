from domain.errors import DomainError


class ReadOnlyField(DomainError):
    def __init__(self, field: str):
        super().__init__(
            message=f'Field {field} is read-only',
            field=field
        )
