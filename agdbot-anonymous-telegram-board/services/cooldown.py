import time


class CooldownService:
    def __init__(self, cooldown_seconds: float) -> None:
        self._cooldown_seconds = cooldown_seconds
        self._last_post_at: dict[int, float] = {}

    def is_on_cooldown(self, user_id: int) -> bool:
        last_post_at = self._last_post_at.get(user_id)
        if last_post_at is None:
            return False
        return (time.monotonic() - last_post_at) < self._cooldown_seconds

    def mark_posted(self, user_id: int) -> None:
        self._last_post_at[user_id] = time.monotonic()
