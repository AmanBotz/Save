# ---------------------------------------------------
# File Name: speedtest.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from time import time
from speedtest import Speedtest
import math
from telethon import events
from devgagan import botStartTime
from devgagan import sex as gagan

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'file too large'


@gagan.on(events.NewMessage(incoming=True, pattern='/speedtest'))
async def speedtest(event):
    speed = await event.reply("ʀᴜɴɴɪɴɢ ꜱᴘᴇᴇᴅᴛᴇꜱᴛ. ᴡᴀɪᴛ ᴀʙᴏᴜᴛ ꜱᴏᴍᴇ ꜱᴇᴄꜱ.")  # edit telethon
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = result['share']
    currentTime = get_readable_time(time() - botStartTime)
    string_speed = f'''
╭─《 🚀 ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ɪɴꜰᴏ 》
├ <b>ᴜᴘʟᴏᴀᴅ:</b> <code>{speed_convert(result['upload'], False)}</code>
├ <b>ᴅᴏᴡɴʟᴏᴀᴅ:</b> <code>{speed_convert(result['download'], False)}</code>
├ <b>ᴘɪɴɢ:</b> <code>{result['ping']} ms</code>
├ <b>ᴛɪᴍᴇ:</b> <code>{result['timestamp']}</code>
├ <b>ᴅᴀᴛᴀ ꜱᴇɴᴛ:</b> <code>{get_readable_file_size(int(result['bytes_sent']))}</code>
╰ <b>ᴅᴀᴛᴀ ʀᴇᴄᴇɪᴠᴇᴅ:</b> <code>{get_readable_file_size(int(result['bytes_received']))}</code>
╭─《 🌐 ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ꜱᴇʀᴠᴇʀ 》
├ <b>ɴᴀᴍᴇ:</b> <code>{result['server']['name']}</code>
├ <b>ᴄᴏᴜɴᴛʀʏ:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
├ <b>ꜱᴘᴏɴꜱᴏʀ:</b> <code>{result['server']['sponsor']}</code>
├ <b>ʟᴀᴛᴇɴᴄʏ:</b> <code>{result['server']['latency']}</code>
├ <b>ʟᴀᴛɪᴛᴜᴅᴇ:</b> <code>{result['server']['lat']}</code>
╰ <b>ʟᴏɴɢɪᴛᴜᴅᴇ:</b> <code>{result['server']['lon']}</code>
╭─《 👤 ᴄʟɪᴇɴᴛ ᴅᴇᴛᴀɪʟꜱ 》
├ <b>ɪᴘ ᴀᴅᴅʀᴇꜱꜱ:</b> <code>{result['client']['ip']}</code>
├ <b>ʟᴀᴛɪᴛᴜᴅᴇ:</b> <code>{result['client']['lat']}</code>
├ <b>ʟᴏɴɢɪᴛᴜᴅᴇ:</b> <code>{result['client']['lon']}</code>
├ <b>ᴄᴏᴜɴᴛʀʏ:</b> <code>{result['client']['country']}</code>
├ <b>ɪꜱᴘ:</b> <code>{result['client']['isp']}</code>
├ <b>ɪꜱᴘ ʀᴀᴛɪɴɢ:</b> <code>{result['client']['isprating']}</code>
╰ <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴍᴀɴ ʙᴏᴛꜱ</b> 
'''
    try:
        await event.reply(string_speed, file=path, parse_mode='html')
        await speed.delete()
    except Exception as g:
        await speed.delete()
        await event.reply(string_speed, parse_mode='html')

def speed_convert(size, byte=True):
    if not byte: size = size / 8
    power = 2 ** 10
    zero = 0
    units = {0: "B/s", 1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"