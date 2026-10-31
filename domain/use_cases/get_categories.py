from uuid import UUID

from domain.crud import CRUD
from domain.entities.category import CategoryType


class GetCategories:
    def __init__(
        self,
        crud: CRUD,
        user_id: UUID,
        q: str | None = None,
        type: CategoryType | None = None
    ):
        self.__crud = crud
        self.__user_id = user_id
        self.__q = q
        self.__type = type

    async def execute(self):
        return await self.__crud.categories.get_by_query(
            self.__user_id,
            q=self.__q,
            type=self.__type
        )
