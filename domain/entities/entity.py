from datetime import datetime
from uuid import UUID

from .errors import PostingRuleNotDefineForEvent
from domain.core import Event, PostingRule


class Entity:
    def __init__(
        self,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at

    async def process_event(self, event: Event):
        posting_rule = self._find_posting_rule_for_event(event)

        await posting_rule.process(event)

    def _find_posting_rule_for_event(self, event: Event) -> PostingRule:
        raise PostingRuleNotDefineForEvent(event.type)
