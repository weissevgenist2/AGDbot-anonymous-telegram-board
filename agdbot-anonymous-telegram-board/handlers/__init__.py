from aiogram import Router

from handlers import channel_posts, commands, cooldown_callbacks, private_messages


def setup_routers() -> Router:
    root = Router(name="root")
    root.include_router(commands.router)
    root.include_router(cooldown_callbacks.router)
    root.include_router(private_messages.router)
    root.include_router(channel_posts.router)
    return root
