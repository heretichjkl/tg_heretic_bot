class THeretic:
    def __init__(self):
        self.running = True
        self.users = []

class Privileges:
    def __init__(self, is_owner=False, can_play=False, can_download=False):
        self.is_owner = is_owner
        self.can_play = can_play
        self.can_download = can_download

class User:
    def __init__(self, uid=None):
        self.uid = uid
        self.privs = Privileges()
