import asyncio

from pytgcalls import PyTgCalls, idle

from clients import tgcalls
from utils.log import log_reply

async def tgcall_play(ev, media):
    await tgcalls.play(ev.chat_id, media);

async def tgcall_music(ev, media):
    await log_reply('Idi naxui', ev)

async def tgcall_stop(ev):
    await tgcalls.leave_call(ev.chat_id)

async def tgcall_pause(ev):
    await tgcalls.pause(ev.chat_id)
