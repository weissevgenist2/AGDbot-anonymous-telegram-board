import uuid


def new_hold_id() -> str:
    return uuid.uuid4().hex[:12]
