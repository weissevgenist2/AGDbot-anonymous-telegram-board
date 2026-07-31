from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class HeldMessage:
    id: str
    user_id: int
    chat_id: int
    message_id: int
    is_forwarded: bool
    service_message_id: int | None = None


class HeldMessageStore(Protocol):
    async def create(
        self,
        *,
        hold_id: str,
        user_id: int,
        chat_id: int,
        message_id: int,
        is_forwarded: bool,
    ) -> HeldMessage: ...

    async def get(self, hold_id: str) -> HeldMessage | None: ...

    async def set_service_message_id(self, hold_id: str, service_message_id: int) -> None: ...

    async def remove(self, hold_id: str) -> HeldMessage | None: ...


class InMemoryHeldMessageStore:
    def __init__(self) -> None:
        self._items: dict[str, HeldMessage] = {}

    async def create(
        self,
        *,
        hold_id: str,
        user_id: int,
        chat_id: int,
        message_id: int,
        is_forwarded: bool,
    ) -> HeldMessage:
        held = HeldMessage(
            id=hold_id,
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            is_forwarded=is_forwarded,
        )
        self._items[hold_id] = held
        return held

    async def get(self, hold_id: str) -> HeldMessage | None:
        return self._items.get(hold_id)

    async def set_service_message_id(self, hold_id: str, service_message_id: int) -> None:
        held = self._items.get(hold_id)
        if held is not None:
            held.service_message_id = service_message_id

    async def remove(self, hold_id: str) -> HeldMessage | None:
        return self._items.pop(hold_id, None)
