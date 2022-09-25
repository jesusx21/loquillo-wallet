class CategoriesParentCategories:
    def __init__(self, db, category_id, parent_category_id):
        self.db = db
        self._category_id = category_id
        self._parent_category = parent_category_id