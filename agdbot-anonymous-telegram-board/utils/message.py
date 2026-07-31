from aiogram.types import Message


def is_forwarded(message: Message) -> bool:
    return bool(
        message.forward_origin
        or message.forward_from
        or message.forward_from_chat
        or message.forward_sender_name
    )
