from .stores import InMemoryDatabase


def get_database() -> InMemoryDatabase:
    return InMemoryDatabase()
