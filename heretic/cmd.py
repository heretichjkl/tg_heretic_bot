import asyncio
from os import remove

import telethon

from clients import client
from utils.yt import cli_to_api, ydl_download, update_opts, ydl_get_title
from utils.tg import send_file
import utils.tg as tg
from utils.call import *
from utils.log import log, log_reply
from utils.db import is_user, add_user, delete_user, update_privilege
from utils.utils import get_hash
from structs import User, Privileges

def is_privileged(usr_privs: Privileges, privs: Privileges):
    permit = True

    if usr_privs.is_owner == True:
        return True

    if usr_privs.can_play < privs.can_play:
        permit = False
    if usr_privs.can_download < privs.can_download:
        permit = False

    return permit

async def run_privileged(ev, usr_privs: Privileges, privs: Privileges,
                         func, *args, **kv_args):
    if is_privileged(usr_privs, privs):
        await func(*args, **kv_args)
    else:
        await log_reply('Lacking privileges.', ev)

async def register_user(ev, args):
    if len(args) > 0:
        ent = await tg.get_user(args[0])
        if ent:
            add_user(ent.user_id)
        else:
            await log_reply('Not a user', ev)
    else:
        await log_reply('No input username', ev)

async def unregister_user(ev, args):
    if len(args) > 0:
        ent = await tg.get_user(args[0])
        if ent:
            delete_user(ent.user_id)
        else:
            await log_reply('Not a user', ev)
    else:
        await log_reply('No input username', ev)

async def set_privilege(ev, args):
    if len(args) < 2:
        await log_reply('Not enough arguments', ev)

    permit = False
    if args[0][0] == '+':
        permit = True

    args[0] = args[0][1:]

    ent = await tg.get_user(args[1])
    if ent == None:
        await log_reply('Not a user', ev)
        return

    if not is_user(ent.user_id):
        await log_reply('Such user isn\'t registered', ev)
        return

    update_privilege(ent.user_id, args[0], permit)

async def cmd_play(usr, ev, args):
    privs = Privileges(can_play=True)
    await run_privileged(ev, usr.privs, privs, tgcall_play, ev, args[0])

async def cmd_music(usr, ev, args):
    privs = Privileges(can_play=True)
    await run_privileged(ev, usr.privs, privs, tgcall_music, ev, args[0])

async def cmd_stop(usr, ev, args):
    privs = Privileges(can_play=True)
    await run_privileged(ev, usr.privs, privs, tgcall_stop, ev)

async def cmd_pause(usr, ev, args):
    privs = Privileges(can_play=True)
    await run_privileged(ev, usr.privs, privs, tgcall_pause, ev)

async def cmd_register(usr, ev, args):
    privs = Privileges(is_owner=True)
    await run_privileged(ev, usr.privs, privs, register_user, ev, args)

async def cmd_unregister(usr, ev, args):
    privs = Privileges(is_owner=True)
    await run_privileged(ev, usr.privs, privs, unregister_user, ev, args)

async def cmd_whoami(usr, ev, args):
    sender = await ev.get_sender()
    await log_reply(str(sender.id), ev);

async def cmd_set_privilege(usr, ev, args):
    privs = Privileges(is_owner=True)
    await run_privileged(ev, usr.privs, privs, set_privilege, ev, args)

async def cmd_ytm(usr, ev, args):
    privs = Privileges(can_download=True)
    if not is_privileged(usr.privs, privs):
        await log_reply('Fuck yourself in a mouth with a cactus', ev)
        return

    try:
        opts = cli_to_api(
            ['--extract-audio', '--audio-format=mp3', '--embed-metadata']
        )
        opts = update_opts(opts)

        for link in args:
            title = ydl_get_title(link)
            s = await ev.get_sender()
            h = get_hash(title, str(s.id))

            opts['outtmpl'] = h + '.%(ext)s'
            fname = ydl_download(opts, args[0])

            if fname:
                await send_file(ev, fname, title=title+'.mp3', delete=True)
            else:
                await log_reply('Err :<', ev)
    except IndexError:
        await log_reply("Link is absent.", ev)

cmd_dict = {
    'ytm': cmd_ytm,
    'whoami': cmd_whoami,
    'register': cmd_register,
    'unregister': cmd_unregister,
    'set_privilege': cmd_set_privilege,
    'play': cmd_play,
    'music': cmd_music,
    'stop': cmd_stop,
    'pause': cmd_pause,
}

async def do_cmd(usr: User, ev, args):
    if len(args):
        try:
            if args[0] in cmd_dict.keys():
                await cmd_dict[args[0]](usr, ev, args[1:])
            else:
                await log_reply('Invalid command.', ev)
        except IndexError:
            await log_reply('U R So Fucked [HD] (OutOfBoundary)', ev)

