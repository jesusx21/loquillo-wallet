from enum import Enum
from uuid import UUID

from .entity import Entity


class CategoryType(Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    DEBT = 'debt'
    LOAN = 'loan'


class Category(Entity):
    def __init__(
        self,
        user_id: UUID,
        name: str,
        type: CategoryType,
        id: str | None = None,
        account_id: UUID | None = None,
        parent_category_id: UUID | None = None,
        created_at: str | None = None,
        updated_at: str | None = None
    ):
        super().__init__(id, created_at, updated_at)

        self.user_id = user_id
        self.name = name
        self.type = type
        self.account_id = account_id
        self.parent_category_id = parent_category_id
