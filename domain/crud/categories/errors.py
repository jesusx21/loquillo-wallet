from uuid import UUID

from domain.errors import DomainError, NotFound


class CouldNotGetCategory(DomainError):
    def __init__(self, category_id: UUID, cause: Exception):
        super().__init__(
            f'Could not get category with ID {category_id}',
            cause=cause,
            category_id=category_id
        )


class CouldNotGetCategories(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(
            'Could not get categories',
            cause=cause
        )


class CategoryNotFound(NotFound):
    def __init__(self, category_id: str):
        super().__init__(
            message=f'Category with ID {category_id} not found',
            category_id=category_id
        )


class CouldNotCreateCategory(DomainError):
    def __init__(self, cause: Exception = None, **kwargs):
        super().__init__(
            message='Could not create category', cause=cause, **kwargs
        )
