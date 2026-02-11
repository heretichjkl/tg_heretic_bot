from os import remove

from telethon import TelegramClient
from telethon.tl.types import InputPeerUser

from clients import client
from utils.log import log, log_reply

async def send_file(ev, fname, title=None, delete=False):
    log(f'Sending file to server: {fname}')
    hndl = None

    if title:
        hndl = await client.upload_file(fname, file_name=title)
    else:
        hndl = await client.upload_file(fname)

    await client.send_file(ev.chat_id, hndl)

    if delete:
        log(f'Deleting: {fname}')
        remove(fname)

async def get_user(usrname):
    ent = await client.get_input_entity(usrname)
    if isinstance(ent, InputPeerUser):
        return ent
    else:
        return None
