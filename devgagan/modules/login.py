# ---------------------------------------------------
# File Name: login.py
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

from pyrogram import filters, Client
from devgagan import app
import random
import os
import asyncio
import string
from devgagan.core.mongo import db
from devgagan.core.func import subscribe, chk_user
from config import API_ID as api_id, API_HASH as api_hash
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait
)

def generate_random_name(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))  # Editted ... 

async def delete_session_files(user_id):
    session_file = f"session_{user_id}.session"
    memory_file = f"session_{user_id}.session-journal"

    session_file_exists = os.path.exists(session_file)
    memory_file_exists = os.path.exists(memory_file)

    if session_file_exists:
        os.remove(session_file)
    
    if memory_file_exists:
        os.remove(memory_file)

    # Delete session from the database
    if session_file_exists or memory_file_exists:
        await db.remove_session(user_id)
        return True  # Files were deleted
    return False  # No files found

@app.on_message(filters.command("logout"))
async def clear_db(client, message):
    user_id = message.chat.id
    files_deleted = await delete_session_files(user_id)
    try:
        await db.remove_session(user_id)
    except Exception:
        pass

    if files_deleted:
        await message.reply("✅ ʏᴏᴜʀ ꜱᴇssɪᴏɴ ᴅᴀᴛᴀ ᴀɴᴅ ꜰɪʟᴇꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴄʟᴇᴀʀᴇᴅ ꜰʀᴏᴍ ᴍᴇᴍᴏʀʏ ᴀɴᴅ ᴅɪꜱᴋ.")
    else:
        await message.reply("✅ ʟᴏɢɢᴇᴅ ᴏᴜᴛ ᴡɪᴛʜ ꜰʟᴀɢ -ᴍ")
        
    
@app.on_message(filters.command("login"))
async def generate_session(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return
        
    # user_checked = await chk_user(message, message.from_user.id)
    # if user_checked == 1:
        # return
        
    user_id = message.chat.id   
    
    number = await _.ask(user_id, "ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ. \nᴇxᴀᴍᴘʟᴇ: +19876543210", filters=filters.text)   
    phone_number = number.text
    try:
        await message.reply("📲 ꜱᴇɴᴅɪɴɢ ᴏᴛᴘ...")
        client = Client(f"session_{user_id}", api_id, api_hash)
        
        await client.connect()
    except Exception as e:
        await message.reply(f"❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴇɴᴅ ᴏᴛᴘ {e}. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
    try:
        code = await client.send_code(phone_number)
    except ApiIdInvalid:
        await message.reply("❌ ɪɴᴠᴀʟɪᴅ ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ᴏғ ᴀᴘɪ ɪᴅ ᴀɴᴅ ᴀᴘɪ ʜᴀsʜ. ᴘʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ꜱᴇssɪᴏɴ.")
        return
    except PhoneNumberInvalid:
        await message.reply("❌ ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ. ᴘʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ꜱᴇssɪᴏɴ.")
        return
    try:
        otp_code = await _.ask(user_id, "ᴇɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴘ ɪɴ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ꜰᴏʀᴍᴀᴛ: \nɪꜰ ᴛʜᴇ ᴏᴛᴘ ɪꜱ `12345`, ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ɪᴛ ᴀꜱ `1 2 3 4 5`.", filters=filters.text, timeout=600)
    except TimeoutError:
        await message.reply("⏰ ᴛɪᴍᴇ ʟɪᴍɪᴛ ᴏꜰ 10 ᴍɪɴᴜᴛᴇꜱ ᴇxᴄᴇᴇᴅᴇᴅ. ᴘʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ꜱᴇssɪᴏɴ.")
        return
    phone_code = otp_code.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
                
    except PhoneCodeInvalid:
        await message.reply("❌ ɪɴᴠᴀʟɪᴅ ᴏᴛᴘ. ᴘʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ꜱᴇssɪᴏɴ.")
        return
    except PhoneCodeExpired:
        await message.reply("❌ ᴇxᴘɪʀᴇᴅ ᴏᴛᴘ. ᴘʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ꜱᴇssɪᴏɴ.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_msg = await _.ask(user_id, "ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀꜱ ᴛᴡᴏ-ꜱᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴇɴᴀʙʟᴇᴅ. ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴘᴀꜱꜱᴡᴏʀᴅ.", filters=filters.text, timeout=300)
        except TimeoutError:
            await message.reply("⏰ ᴛɪᴍᴇ ʟɪᴍɪᴛ ᴏꜰ 5 ᴍɪɴᴜᴛᴇꜱ ᴇxᴄᴇᴇᴅᴇᴅ. ᴘʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ꜱᴇssɪᴏɴ.")
            return
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply("❌ ɪɴᴠᴀʟɪᴅ ᴘᴀꜱꜱᴡᴏʀᴅ. ᴘʟᴇᴀsᴇ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ꜱᴇssɪᴏɴ.")
            return
    string_session = await client.export_session_string()
    await db.set_session(user_id, string_session)
    await client.disconnect()
    await otp_code.reply("✅ ʟᴏɢɪɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ!")