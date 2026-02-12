import asyncio
import argparse
import os

from telethon import TelegramClient, functions, types, events

from clients import client, tgcalls, IS_BOT
from utils.yt import cli_to_api, ydl_download
from utils.db import init_db, is_user, fetch_user
from utils.log import log, log_reply
import utils.call
from cmd import *
from structs import *
import config
from config import STORAGE_PATH

_cmd_prefix = config.CMD_PREFIX

def get_args(s) -> list[str]:
    global _cmd_prefix
    return s.removeprefix(_cmd_prefix).strip().split()

async def init_ev_hndl(Heretic: THeretic):
    @client.on(events.NewMessage(pattern=_cmd_prefix + '*'))
    async def handle_new_message(event):
        sender = await event.get_sender()
        usr = fetch_user(sender.id)

        if usr:
            args = get_args(event.raw_text)
            args_str = ' '.join(args)

            log(f'ID:%s USER:%s CMD:%s'
                % (str(sender.id), sender.username, args_str))

            await do_cmd(usr, event, args)
        else:
            await log_reply('Unauthorized', event)

async def init_main() -> THeretic:
    Heretic = THeretic()

    await client.start(bot_token=config.TG_API_BOT if IS_BOT else None)
    await tgcalls.start()

    return Heretic

async def init() -> THeretic:
    if not os.path.isdir(STORAGE_PATH):
        os.mkdir(STORAGE_PATH)

    Heretic = await init_main()
    log("STARTED")

    await init_db()
    await init_ev_hndl(Heretic)

    return Heretic

async def main_loop(Heretic):
        await asyncio.sleep(5)

async def main():
    Heretic = await init()
    while Heretic.running:
        await main_loop(Heretic)

    client.disconnect()

def halt():
    log('SHUTDOWN')

if __name__ == '__main__':
    prs = argparse.ArgumentParser()
    prs.add_argument('--setup', action='store_true',
                     help='Set some configuration')
    args = prs.parse_args()

    try:
        if args.setup:
            print("setup")
        try:
            asyncio.get_event_loop().run_until_complete(main())
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop()).run_until_complete(main())
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')
        halt()

    halt()
