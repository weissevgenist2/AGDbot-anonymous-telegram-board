class InMemorySubscriberStore:
    def __init__(self) -> None:
        self._subscribers: set[int] = set()

    async def add(self, user_id: int) -> None:
        self._subscribers.add(user_id)

    async def remove(self, user_id: int) -> None:
        self._subscribers.discard(user_id)

    async def contains(self, user_id: int) -> bool:
        return user_id in self._subscribers

    async def get_all(self) -> list[int]:
        return list(self._subscribers)


class InMemoryPostTracker:
    def __init__(self) -> None:
        self._authors: dict[int, int] = {}

    async def mark_author_post(self, channel_message_id: int, user_id: int) -> None:
        self._authors[channel_message_id] = user_id

    async def pop_author(self, channel_message_id: int) -> int | None:
        return self._authors.pop(channel_message_id, None)
