# ---------------------------------------------------
# File Name: main.py
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
# More readable 
# ---------------------------------------------------

import time
import random
import string
import asyncio
from pyrogram import filters, Client
from devgagan import app, userrbot
from config import API_ID, API_HASH, FREEMIUM_LIMIT, PREMIUM_LIMIT, OWNER_ID, DEFAULT_SESSION
from devgagan.core.get_func import get_msg
from devgagan.core.func import *
from devgagan.core.mongo import db
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess
from devgagan.modules.shrink import is_user_verified

async def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

users_loop = {}
interval_set = {}
batch_mode = {}

async def process_and_upload_link(userbot, user_id, msg_id, link, retry_count, message):
    try:
        await get_msg(userbot, user_id, msg_id, link, retry_count, message)
        try:
            await app.delete_messages(user_id, msg_id)
        except Exception:
            pass
        await asyncio.sleep(15)
    finally:
        pass

# Function to check if the user can proceed
async def check_interval(user_id, freecheck):
    if freecheck != 1 or await is_user_verified(user_id):  # Premium or owner users can always proceed
        return True, None

    now = datetime.now()

    # Check if the user is on cooldown
    if user_id in interval_set:
        cooldown_end = interval_set[user_id]
        if now < cooldown_end:
            remaining_time = (cooldown_end - now).seconds
            return False, f"ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ {remaining_time} ѕᴇᴄᴏɴᴅѕ(ѕ) ʙᴇғᴏʀᴇ ѕᴇɴᴅɪɴɢ ᴀɴᴏᴛʜᴇʀ ʟɪɴᴋ. ᴀʟᴛᴇʀɴᴀᴛɪᴠᴇʟʏ, ᴘᴜʀᴄʜᴀsᴇ ᴘʀᴇᴍɪᴜᴍ ꜰᴏʀ ɪɴsᴛᴀɴᴛ ᴀᴄᴄᴇss.\n\n> ʜᴇʏ 👋 ʏᴏᴜ ᴄᴀɴ ᴜsᴇ /ᴛᴏᴋᴇɴ ᴛᴏ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ ꜰʀᴇᴇ ꜰᴏʀ 3 ʜᴏᴜʀs ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴛɪᴍᴇ ʟɪᴍɪᴛ."
        else:
            del interval_set[user_id]  # Cooldown expired, remove user from interval set

    return True, None

async def set_interval(user_id, interval_minutes=45):
    now = datetime.now()
    # Set the cooldown interval for the user
    interval_set[user_id] = now + timedelta(seconds=interval_minutes)
    
@app.on_message(
    filters.regex(r'https?://(?:www\.)?t\.me/[^\s]+|tg://openmessage\?user_id=\w+&message_id=\d+')
    & filters.private
)
async def single_link(_, message):
    user_id = message.chat.id

    # Check subscription and batch mode
    if await subscribe(_, message) == 1 or user_id in batch_mode:
        return

    # Check if user is already in a loop
    if users_loop.get(user_id, False):
        await message.reply(
            "ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀɴ ᴏɴɢᴏɪɴɢ ᴘʀᴏᴄᴇss. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ꜰᴏʀ ɪᴛ ᴛᴏ ꜰɪɴɪꜱʜ ᴏʀ ᴄᴀɴᴄᴇʟ ɪᴛ ᴡɪᴛʜ /ᴄᴀɴᴄᴇʟ."
        )
        return

    # Check freemium limits
    if await chk_user(message, user_id) == 1 and FREEMIUM_LIMIT == 0 and user_id not in OWNER_ID and not await is_user_verified(user_id):
        await message.reply("ꜰʀᴇᴇᴍɪᴜᴍ ꜱᴇʀᴠɪᴄᴇ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ. ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ꜰᴏʀ ᴀᴄᴄᴇss.")
        return

    # Check cooldown
    can_proceed, response_message = await check_interval(user_id, await chk_user(message, user_id))
    if not can_proceed:
        await message.reply(response_message)
        return

    # Add user to the loop
    users_loop[user_id] = True

    link = message.text if "tg://openmessage" in message.text else get_link(message.text)
    msg = await message.reply("ᴘʀᴏᴄᴇssɪɴɢ...")
    userbot = await initialize_userbot(user_id)
    try:
        if await is_normal_tg_link(link):
            await process_and_upload_link(userbot, user_id, msg.id, link, 0, message)
            await set_interval(user_id, interval_minutes=45)
        else:
            await process_special_links(userbot, user_id, msg, link)
            
    except FloodWait as fw:
        await msg.edit_text(f"ᴛʀʏ ᴀɢᴀɪɴ ᴀꜰᴛᴇʀ {fw.x} ѕᴇᴄᴏɴᴅꜱ ᴅᴜᴇ ᴛᴏ ꜰʟᴏᴏᴅᴡᴀɪᴛ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ.")
    except Exception as e:
        await msg.edit_text(f"ʟɪɴᴋ: `{link}`\n\n**ᴇʀʀᴏʀ:** {str(e)}")
    finally:
        users_loop[user_id] = False
        try:
            await msg.delete()
        except Exception:
            pass

async def initialize_userbot(user_id):  # this ensure the single startup .. even if logged in or not
    data = await db.get_data(user_id)
    if data and data.get("session"):
        try:
            device = 'iPhone 16 Pro'  # added gareebi text
            userbot = Client(
                "userbot",
                api_id=API_ID,
                api_hash=API_HASH,
                device_model=device,
                session_string=data.get("session")
            )
            await userbot.start()
            return userbot
        except Exception:
            await app.send_message(user_id, "ʟᴏɢɪɴ ᴇxᴘɪʀᴇᴅ ʀᴇ ᴅᴏ ʟᴏɢɪɴ")
            return None
    else:
        if DEFAULT_SESSION:
            return userrbot
        else:
            return None

async def is_normal_tg_link(link: str) -> bool:
    """Check if the link is a standard Telegram link."""
    special_identifiers = ['t.me/+', 't.me/c/', 't.me/b/', 'tg://openmessage']
    return 't.me/' in link and not any(x in link for x in special_identifiers)
    
async def process_special_links(userbot, user_id, msg, link):
    if userbot is None:
        return await msg.edit_text("ᴛʀʏ ʟᴏɢɪɴɢ ɪɴ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.")
    if 't.me/+' in link:
        result = await userbot_join(userbot, link)
        await msg.edit_text(result)
        return
    special_patterns = ['t.me/c/', 't.me/b/', '/s/', 'tg://openmessage']
    if any(sub in link for sub in special_patterns):
        await process_and_upload_link(userbot, user_id, msg.id, link, 0, msg)
        await set_interval(user_id, interval_minutes=45)
        return
    await msg.edit_text("ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ...")

@app.on_message(filters.command("batch") & filters.private)
async def batch_link(_, message):
    join = await subscribe(_, message)
    if join == 1:
        return
    user_id = message.chat.id
    # Check if a batch process is already running
    if users_loop.get(user_id, False):
        await app.send_message(
            message.chat.id,
            "ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀ ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇss ʀᴜɴɴɪɴɢ. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ꜰᴏʀ ɪᴛ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ."
        )
        return

    freecheck = await chk_user(message, user_id)
    if freecheck == 1 and FREEMIUM_LIMIT == 0 and user_id not in OWNER_ID and not await is_user_verified(user_id):
        await message.reply("ꜰʀᴇᴇᴍɪᴜᴍ ꜱᴇʀᴠɪᴄᴇ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ. ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ꜰᴏʀ ᴀᴄᴄᴇss.")
        return

    max_batch_size = FREEMIUM_LIMIT if freecheck == 1 else PREMIUM_LIMIT

    # Start link input
    for attempt in range(3):
        start = await app.ask(message.chat.id, "ᴘʟᴇᴀsᴇ ꜱᴇɴᴅ ᴛʜᴇ ꜱᴛᴀʀᴛ ʟɪɴᴋ.\n\n> ᴍᴀxɪᴍᴜᴍ ᴛʀɪᴇꜱ 3")
        start_id = start.text.strip()
        s = start_id.split("/")[-1]
        if s.isdigit():
            cs = int(s)
            break
        await app.send_message(message.chat.id, "ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ. ᴘʟᴇᴀsᴇ ꜱᴇɴᴅ ᴀɢᴀɪɴ ...")
    else:
        await app.send_message(message.chat.id, "ᴍᴀxɪᴍᴜᴍ ᴀᴛᴛᴇᴍᴘᴛꜱ ᴇxᴄᴇᴇᴅᴇᴅ. ᴛʀʏ ʟᴀᴛᴇʀ.")
        return

    # Number of messages input
    for attempt in range(3):
        num_messages = await app.ask(message.chat.id, f"ʜᴏᴡ ᴍᴀɴʏ ᴍᴇꜱꜱᴀɢᴇꜱ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʀᴏᴄᴇss?\n> ᴍᴀx ʟɪᴍɪᴛ {max_batch_size}")
        try:
            cl = int(num_messages.text.strip())
            if 1 <= cl <= max_batch_size:
                break
            raise ValueError()
        except ValueError:
            await app.send_message(
                message.chat.id, 
                f"ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ. ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ɴᴜᴍʙᴇʀ ʙᴇᴛᴡᴇᴇɴ 1 ᴀɴᴅ {max_batch_size}."
            )
    else:
        await app.send_message(message.chat.id, "ᴍᴀxɪᴍᴜᴍ ᴀᴛᴛᴇᴍᴘᴛꜱ ᴇxᴄᴇᴇᴅᴇᴅ. ᴛʀʏ ʟᴀᴛᴇʀ.")
        return

    # Validate and interval check
    can_proceed, response_message = await check_interval(user_id, freecheck)
    if not can_proceed:
        await message.reply(response_message)
        return
        
    join_button = InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/amanbots")
    keyboard = InlineKeyboardMarkup([[join_button]])
    pin_msg = await app.send_message(
        user_id,
        f"ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇss ꜱᴛᴀʀᴛᴇᴅ ⚡\nᴘʀᴏᴄᴇssɪɴɢ: 0/{cl}\n\n**ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴍᴀɴ ʙᴏᴛꜱ**",
        reply_markup=keyboard
    )
    await pin_msg.pin(both_sides=True)

    users_loop[user_id] = True
    try:
        normal_links_handled = False
        userbot = await initialize_userbot(user_id)
        # Handle normal links first
        for i in range(cs, cs + cl):
            if user_id in users_loop and users_loop[user_id]:
                url = f"{'/'.join(start_id.split('/')[:-1])}/{i}"
                link = get_link(url)
                # Process t.me links (normal) without userbot
                if 't.me/' in link and not any(x in link for x in ['t.me/b/', 't.me/c/', 'tg://openmessage']):
                    msg = await app.send_message(message.chat.id, "ᴘʀᴏᴄᴇssɪɴɢ...")
                    await process_and_upload_link(userbot, user_id, msg.id, link, 0, message)
                    await pin_msg.edit_text(
                        f"ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇss ꜱᴛᴀʀᴛᴇᴅ ⚡\nᴘʀᴏᴄᴇssɪɴɢ: {i - cs + 1}/{cl}\n\n**__ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴍᴀɴ ʙᴏᴛꜱ__**",
                        reply_markup=keyboard
                    )
                    normal_links_handled = True
        if normal_links_handled:
            await set_interval(user_id, interval_minutes=300)
            await pin_msg.edit_text(
                f"ʙᴀᴛᴄʜ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ꜰᴏʀ {cl} ᴍᴇꜱꜱᴀɢᴇꜱ 🎉\n\n**__ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴍᴀɴ ʙᴏᴛꜱ__**",
                reply_markup=keyboard
            )
            await app.send_message(message.chat.id, "ʙᴀᴛᴄʜ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ! 🎉")
            return
            
        # Handle special links with userbot
        for i in range(cs, cs + cl):
            if not userbot:
                await app.send_message(message.chat.id, "ʟᴏɢɪɴ ɪɴ ʙᴏᴛ ꜰɪʀꜱᴛ ...")
                users_loop[user_id] = False
                return
            if user_id in users_loop and users_loop[user_id]:
                url = f"{'/'.join(start_id.split('/')[:-1])}/{i}"
                link = get_link(url)
                if any(x in link for x in ['t.me/b/', 't.me/c/']):
                    msg = await app.send_message(message.chat.id, "ᴘʀᴏᴄᴇssɪɴɢ...")
                    await process_and_upload_link(userbot, user_id, msg.id, link, 0, message)
                    await pin_msg.edit_text(
                        f"ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇss ꜱᴛᴀʀᴛᴇᴅ ⚡\nᴘʀᴏᴄᴇssɪɴɢ: {i - cs + 1}/{cl}\n\n**__ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴍᴀɴ ʙᴏᴛꜱ__**",
                        reply_markup=keyboard
                    )

        await set_interval(user_id, interval_minutes=300)
        await pin_msg.edit_text(
            f"ʙᴀᴛᴄʜ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ꜰᴏʀ {cl} ᴍᴇꜱꜱᴀɢᴇꜱ 🎉\n\n**__ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴍᴀɴ ʙᴏᴛꜱ__**",
            reply_markup=keyboard
        )
        await app.send_message(message.chat.id, "ʙᴀᴛᴄʜ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ! 🎉")

    except Exception as e:
        await app.send_message(message.chat.id, f"ᴇʀʀᴏʀ: {e}")
    finally:
        users_loop.pop(user_id, None)

@app.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id

    # Check if there is an active batch process for the user
    if user_id in users_loop and users_loop[user_id]:
        users_loop[user_id] = False  # Set the loop status to False
        await app.send_message(
            message.chat.id, 
            "ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇssɪɴɢ ʜᴀꜱ ʙᴇᴇɴ ꜱᴛᴏᴘᴘᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ. ʏᴏᴜ ᴄᴀɴ ꜱᴛᴀʀᴛ ᴀ ɴᴇᴡ ʙᴀᴛᴄʜ ɴᴏᴡ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ."
        )
    elif user_id in users_loop and not users_loop[user_id]:
        await app.send_message(
            message.chat.id, 
            "ᴛʜᴇ ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇss ᴡᴀꜱ ᴀʟʀᴇᴀᴅʏ ꜱᴛᴏᴘᴘᴇᴅ. ɴᴏ ᴀᴄᴛɪᴠᴇ ʙᴀᴛᴄʜ ᴛᴏ ᴄᴀɴᴄᴇʟ."
        )
    else:
        await app.send_message(
            message.chat.id, 
            "ɴᴏ ᴀᴄᴛɪᴠᴇ ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇssɪɴɢ ɪꜱ ʀᴜɴɴɪɴɢ ᴛᴏ ᴄᴀɴᴄᴇʟ."
        )