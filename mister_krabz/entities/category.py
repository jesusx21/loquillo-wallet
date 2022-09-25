from mister_krabz.entities.entity import Entity


class CategoriesParentCategoriesAlreadySet(Exception): pass


class Category(Entity):
    def __init__(
        self,
        name,
        parent_category=None,
        id=None,
        created_at=None,
        updated_at=None,
        categories_parent_categories=None
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        self.name = name
        self._parent_category = parent_category
        self._categories_parent_categories = categories_parent_categories

    def set_categories_parent_categories(self, categories_parent_categories):
        if self._categories_parent_categories:
            raise CategoriesParentCategoriesAlreadySet()
        
        self._categories_parent_categories = categories_parent_categories