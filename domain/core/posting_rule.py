from .event import Event


class PostingRule:
    def process(self, event: Event):
        raise NotImplementedError(f'No process defined for event type {event.type}')
