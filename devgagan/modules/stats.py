import time
import sys
import motor
from devgagan import app
from pyrogram import filters
from config import OWNER_ID
from devgagan.core.mongo.users_db import get_users, add_user, get_user
from devgagan.core.mongo.plans_db import premium_users

start_time = time.time()

@app.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        if message.from_user:
            us_in_db = await get_user(message.from_user.id)
            if not us_in_db:
                await add_user(message.from_user.id)
    except:
        pass

def time_formatter():
    minutes, seconds = divmod(int(time.time() - start_time), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if tmp != "":
        if tmp.endswith(":"):
            return tmp[:-1]
        else:
            return tmp
    else:
        return "0 s"

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    start = time.time()
    users = len(await get_users())
    premium = await premium_users()
    ping = round((time.time() - start) * 1000)
    await message.reply_text(f"""
**ꜱᴛᴀᴛꜱ ᴏꜰ** {(await client.get_me()).mention} :

🏓 **ᴘɪɴɢ ᴘᴏɴɢ**: {ping}ms

📊 **ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ** : `{users}`
📈 **ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ** : `{len(premium)}`
⚙️ **ʙᴏᴛ ᴜᴘᴛɪᴍᴇ** : `{time_formatter()}`

🎨 **ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ**: `{sys.version.split()[0]}`
📑 **ᴍᴏɴɢᴏ ᴠᴇʀꜱɪᴏɴ**: `{motor.version}`
""")