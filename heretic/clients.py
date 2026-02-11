import asyncio

from telethon import TelegramClient
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
from pytgcalls import PyTgCalls

import config

IS_BOT = True if config.TG_API_BOT else False

client = TelegramClient('bot' if IS_BOT else 'anon',
                        config.TG_API_ID, config.TG_API_HASH)
tgcalls = PyTgCalls(client)
