from domain.errors import DomainError
from domain.entities.category import CategoryType


class InvalidCategoryType(DomainError):
    def __init__(self, type: CategoryType):
        message = f"Invalid category type: {type}"

        super().__init__(message, category_type=type)


class InvalidTransactionAmount(DomainError):
    def __init__(self, amount: int):
        message = f"Invalid transaction amount: {amount}"

        super().__init__(message, amount=amount)
