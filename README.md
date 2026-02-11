# tg_heretic_bot

Telegram bot written in python using telethon library for telegram api, pytgcalls and yt-dlp for video player and music downloading.

This is a user bot, which currently can stream video and download music from youtube.
## Setup
After cloning repository copy config.py.example under ./heretic/ folder as config.py, then put your telegram api **ID** and **HASH** in **TG_API_ID** and **TG_API_HASH** variables (if you don't have them yet, get 'em at [my.telegram.org](https://my.telegram.org/auth?to=apps)). Then, telethon may prompt your phone number and password for session, but if you have session file already, copy one as anon.session under repository root. Create python virtual environment and install required modules:
```
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
To run bot, just use python on heretic directory:
```
python ./heretic
```

## How to use
Any user may not use any command without being registered as bot user first. For that, under account bot is running on enter command, substituting someone with real username:
```
hrt>register @someone
```
And, you can unregister user:
```
hrt>unregister @some_faggot
```
Some commands require specific privileges so as for example if someone wants to stream video they would need to have "can_play" privilege. To grant a privilege, use this command:
```
hrt>set_privilege +can_play @someone
```
Also, you can replace + with - to remove privilege:
```
hrt>set_privilege -is_owner @someone
```

Following privileges exists as for now:

* is_owner - Almighty, not given by default.
* can_play - Whether can request video steam, given by default.
* can_download - Can request music to download, not given by default.

All commands available at the moment:
* ytm \<link\> - Download music from youtube.
* whoami - Returns id of your account.
* register \<@someone\> - Register user.
* unregister \<@someone\> - Unregister user.
* set_privilege [+/-]\<privilege\> @someone
* play \<link\> - Stream video to video chat.
* stop - Stop stream.
* pause - Pause stream... Fuck, no unpause!