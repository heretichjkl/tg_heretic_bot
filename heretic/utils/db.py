import sqlite3

from clients import client
from utils.log import log
from structs import User
from config import DB_PATH

_table_schemas = [
    (
    "users ("
    "uid INT PRIMARY KEY NOT NULL UNIQUE,"
    "is_owner INT DEFAULT 0,"
    "can_play INT DEFAULT 0,"
    "can_download INT DEFAULT 0)"
    ),
    (
    "aliases ("
    "owner INT,"
    "alias VARCHAR(25),"
    "definition VARCHAR(255),"
    "FOREIGN KEY(owner) REFERENCES users(uid))"
    ),
]

_needed_tables = {'users', 'aliases'}

def db_connect(db=DB_PATH):
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute("PRAGMA foreign_keys = ON")

    return (con, cur)

def add_user(uid: int):
    con, cur = db_connect()

    cur.execute(f"INSERT INTO users(uid,can_play) VALUES({uid}, 1)")

    con.commit()
    con.close()

def delete_user(uid: int):
    con, cur = db_connect()

    cur.execute(f"DELETE FROM users WHERE uid == {uid}")
    cur.execute(f"DELETE FROM aliases WHERE owner == {uid}")

    con.commit()
    con.close()

def update_privilege(uid, priv_str, positive):
    con, cur = db_connect()

    cur.execute(f"UPDATE users SET {priv_str} = {1 if positive else 0} WHERE uid == {uid}")

    con.commit()
    con.close()

async def init_db():
    con, cur = db_connect()

    rs = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")

    tables = rs.fetchall()
    tables = [t[0] for t in tables]

    if _needed_tables != set(tables):
        log('Missing or redundant tables')

        for t in tables:
            if t not in _needed_tables:
                cur.execute(f"DROP TABLE {t}")
                log(f'DROPPING TABLE {t}')
        con.commit()

    if _needed_tables != set(tables):
        log('Missing tables, dropping existing ones')

        for t in _needed_tables:
            if t in tables:
                cur.execute(f"DROP TABLE {t}")
                log(f'DROPPING TABLE {t}')

        con.commit()

        log('Re-creating tables')
        for ts in _table_schemas:
            cur.execute(f"CREATE TABLE {ts}")
        con.commit()

        me = await client.get_peer_id('me', add_mark=False)
        add_user(me)
        update_privilege(me, 'is_owner', True)
        con.commit()

    con.close()

def is_user(uid: int):
    con, cur = db_connect()
    rs = cur.execute(f"SELECT * FROM users WHERE uid == {uid}")
    usr = rs.fetchone()

    con.close()

    if usr:
        return True

    return False

def fetch_user(uid: int):
    con, cur = db_connect()
    rs = cur.execute(f"SELECT * FROM users WHERE uid == '{uid}'")
    usr_row = rs.fetchone()

    con.close()

    if usr_row:
        usr = User()
        usr.id = usr_row[0]

        usr.privs.is_owner = (True if usr_row[1] == 1 else False)
        usr.privs.can_play = (True if usr_row[2] == 1 else False)
        usr.privs.can_download = (True if usr_row[3] == 1 else False)

        return usr
    return None

