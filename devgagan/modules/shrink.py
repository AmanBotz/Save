# ---------------------------------------------------
# File Name: shrink.py
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

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
import string
import aiohttp
from devgagan import app
from devgagan.core.func import *
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AD_API, LOG_GROUP  
 
 
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]
 
 
async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)
 
 
Param = {}
 
 
async def generate_random_param(length=8):
    """generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
 
 
async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
 
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()   
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None
 
 
async def is_user_verified(user_id):
    """check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None
 
 
@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """handle the /token command."""
    join = await subscribe(client, message)
    if join == 1:
        return
    chat_id = "amanbots"
    msg = await app.get_messages(chat_id, 9)
    user_id = message.chat.id
    if len(message.command) <= 1:
        image_url = "https://i.postimg.cc/mZ14QSBk/IMG-20250303-WA0005.jpg"
        join_button = InlineKeyboardButton("ʝᴏɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/amanbots")
        premium = InlineKeyboardButton("ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ", url="https://t.me/amangodz")   
        keyboard = InlineKeyboardMarkup([
            [join_button],   
            [premium]    
        ])
         
        await message.reply_photo(
            msg.photo.file_id,
            caption=(
                "ʜɪ 👋 ᴡᴇʟᴄᴏᴍᴇ, ᴡᴀɴɴᴀ ɪɴᴛʀᴏ...?\n\n"
                "✳️ ɪ ᴄᴀɴ ꜱᴀᴠᴇ ᴘᴏꜱᴛꜱ ꜰʀᴏᴍ ᴄʜᴀɴɴᴇʟꜱ ᴏʀ ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ꜰᴏʀᴡᴀʀᴅɪɴɢ ɪꜱ ᴏꜰꜰ. ɪ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏꜱ/ᴀᴜᴅɪᴏ ꜰʀᴏᴍ ʏᴛ, ɪɴꜱᴛᴀ, ... ꜱᴏᴄɪᴀʟ ᴘʟᴀᴛꜰᴏʀᴍꜱ.\n"
                "✳️ ꜱɪᴍᴘʟʏ ꜱᴇɴᴅ ᴛʜᴇ ᴘᴏꜱᴛ ʟɪɴᴋ ᴏꜰ ᴀ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟ. ꜰᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ, ᴅᴏ /login. ꜱᴇɴᴅ /help ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ."
            ),
            reply_markup=keyboard
        )
        return  
 
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("ʏᴏᴜ ᴀʀᴇ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ, ɴᴏ ɴᴇᴇᴅ ᴏғ ᴛᴏᴋᴇɴ 😉")
        return
 
    if param:
        if user_id in Param and Param[user_id] == param:
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            })
            del Param[user_id]   
            await message.reply("✅ ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴠᴇʀɪꜰɪᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ! ᴇɴᴊᴏʏ ʏᴏᴜʀ ꜱᴇꜱꜱɪᴏɴ ꜰᴏʀ ɴᴇxᴛ 3 ʜᴏᴜʀꜱ.")
            return
        else:
            await message.reply("❌ ɪɴᴠᴀʟɪᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ. ᴘʟᴇᴀꜱᴇ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ᴛᴏᴋᴇɴ.")
            return
 
@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
     
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("ʏᴏᴜ ᴀʀᴇ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ, ɴᴏ ɴᴇᴇᴅ ᴏғ ᴛᴏᴋᴇɴ 😉")
        return
    if await is_user_verified(user_id):
        await message.reply("✅ ʏᴏᴜʀ ꜰʀᴇᴇ ꜱᴇꜱꜱɪᴏɴ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴇ, ᴇɴᴊᴏʏ!")
    else:
        param = await generate_random_param()
        Param[user_id] = param   
 
        deep_link = f"https://t.me/{client.me.username}?start={param}"
 
        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴛʜᴇ ᴛᴏᴋᴇɴ ʟɪɴᴋ. ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
            return
 
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴠᴇʀɪꜰʏ ᴛʜᴇ ᴛᴏᴋᴇɴ ɴᴏᴡ...", url=shortened_url)]]
        )
        await message.reply(
            "ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴠᴇʀɪꜰʏ ʏᴏᴜʀ ꜰʀᴇᴇ ᴀᴄᴄᴇꜱꜱ ᴛᴏᴋᴇɴ: \n\n> ᴡʜᴀᴛ ᴡɪʟʟ ʏᴏᴜ ɢᴇᴛ ? \n1. ɴᴏ ᴛɪᴍᴇ ʙᴏᴜɴᴅ ᴜᴘᴛᴏ 3 ʜᴏᴜʀꜱ \n2. ʙᴀᴛᴄʜ ᴄᴏᴍᴍᴀɴᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʙᴇ ꜰʀᴇᴇʟɪᴍɪᴛ + 20 \n3. ᴀʟʟ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴜɴʟᴏᴄᴋᴇᴅ",
            reply_markup=button
        )
