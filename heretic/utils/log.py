import asyncio
import datetime
from os import path, mkdir

from telethon import events

from clients import client
import config

async def log_reply_priv(msg, sender):
    """ Reply to person privately """
    await client.send_message(sender, msg);

def log(msg):
    t = datetime.datetime.now()
    log_str = (
        t.strftime('%d.%m.%y-%H:%M:%S')
        + ' '
        + config.CMD_PREFIX
        + msg
    )

    print(log_str)
    log_f_name = path.join(config.STORAGE_PATH, 'log', t.strftime('log_%d.%m.%y.txt'))

    if not path.isdir(path.join(config.STORAGE_PATH, 'log')):
        mkdir(path.join(config.STORAGE_PATH, 'log'))

    with open(log_f_name, 'a') as f:
        f.write(log_str + '\n')

async def log_reply(msg, ev):
    log(msg)
    await ev.reply(config.CMD_PREFIX + ' ' + msg)
