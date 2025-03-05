from pyrogram import filters
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import subscribe
import asyncio
from devgagan.core.func import *
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.raw.functions.bots import SetBotInfo
from pyrogram.raw.types import InputUserSelf

from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
 
@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")
        return
     
    await app.set_bot_commands([
        BotCommand("start", "🚀 ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
        BotCommand("batch", "🫠 ᴇxᴛʀᴀᴄᴛ ɪɴ ʙᴜʟᴋ"),
        BotCommand("login", "🔑 ɢᴇᴛ ɪɴᴛᴏ ᴛʜᴇ ʙᴏᴛ"),
        BotCommand("logout", "🚪 ɢᴇᴛ ᴏᴜᴛ ᴏꜰ ᴛʜᴇ ʙᴏᴛ"),
        BotCommand("token", "🎲 ɢᴇᴛ 3 ʜᴏᴜʀꜱ ꜰʀᴇᴇ ᴀᴄᴄᴇꜱꜱ"),
        BotCommand("adl", "👻 ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴜᴅɪᴏ ꜰʀᴏᴍ 30+ ꜱɪᴛᴇꜱ"),
        BotCommand("dl", "💀 ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏꜱ ꜰʀᴏᴍ 30+ ꜱɪᴛᴇꜱ"),
        BotCommand("transfer", "💘 ɢɪꜰᴛ ᴘʀᴇᴍɪᴜᴍ ᴛᴏ ᴏᴛʜᴇʀꜱ"),
        BotCommand("myplan", "⌛ ɢᴇᴛ ʏᴏᴜʀ ᴘʟᴀɴ ᴅᴇᴛᴀɪʟꜱ"),
        BotCommand("settings", "⚙️ ᴘᴇʀꜱᴏɴᴀʟɪᴢᴇ ᴛʜɪɴɢꜱ"),
        BotCommand("plan", "🗓️ ᴄʜᴇᴄᴋ ᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ"),
        BotCommand("terms", "🥺 ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ"),
        BotCommand("speedtest", "🚅 ꜱᴘᴇᴇᴅ ᴏꜰ ꜱᴇʀᴠᴇʀ"),
        BotCommand("help", "❓ ɪꜰ ʏᴏᴜ'ʀᴇ ᴀ ɴᴏᴏʙ, ꜱᴛɪʟʟ!"),
        BotCommand("cancel", "🚫 ᴄᴀɴᴄᴇʟ ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇꜱꜱ")
    ])
 
    await message.reply("✅ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴏɴꜰɪɢᴜʀᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!")
 
 
help_pages = [
    (
        "📝 **ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ᴏᴠᴇʀᴠɪᴇᴡ (1/2)**:\n\n"
        "1. **/transfer userID**\n"
        "> ᴛʀᴀɴꜱꜰᴇʀ ᴘʀᴇᴍɪᴜᴍ ᴛᴏ ʏᴏᴜʀ ʙᴇʟᴏᴠᴇᴅ ᴍᴀᴊᴏʀ ᴘᴜʀᴘᴏꜱᴇ ꜰᴏʀ ʀᴇꜱᴇʟʟᴇʀꜱ (ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀꜱ ᴏɴʟʏ)\n\n"
        "2. **/lock**\n"
        "> ʟᴏᴄᴋ ᴄʜᴀɴɴᴇʟ ꜰʀᴏᴍ ᴇxᴛʀᴀᴄᴛɪᴏɴ (ᴏᴡɴᴇʀ ᴏɴʟʏ)\n\n"
        "3. **/dl link**\n"
        "> ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏꜱ \n\n"
        "4. **/adl link**\n"
        "> ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴜᴅɪᴏ \n\n"
        "5. **/login**\n"
        "> ʟᴏɢ ɪɴ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ꜰᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴀᴄᴄᴇꜱꜱ\n\n"
        "6. **/batch**\n"
        "> ʙᴜʟᴋ ᴇxᴛʀᴀᴄᴛɪᴏɴ ꜰᴏʀ ᴘᴏꜱᴛꜱ (ᴀꜰᴛᴇʀ ʟᴏɢɪɴ)\n\n"
    ),
    (
        "📝 **ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ᴏᴠᴇʀᴠɪᴇᴡ (2/2)**:\n\n"
        "7. **/logout**\n"
        "> ʟᴏɢ ᴏᴜᴛ ꜰʀᴏᴍ ᴛʜᴇ ʙᴏᴛ\n\n"
        "8. **/plan**\n"
        "> ᴄʜᴇᴄᴋ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ\n\n"
        "9. **/speedtest**\n"
        "> ᴛᴇꜱᴛ ᴛʜᴇ ꜱᴇʀᴠᴇʀ ꜱᴘᴇᴇᴅ\n\n"
        "10. **/terms**\n"
        "> ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ\n\n"
        "11. **/cancel**\n"
        "> ᴄᴀɴᴄᴇʟ ᴏɴɢᴏɪɴɢ ʙᴀᴛᴄʜ ᴘʀᴏᴄᴇꜱꜱ\n\n"
        "12. **/myplan**\n"
        "> ɢᴇᴛ ᴅᴇᴛᴀɪʟꜱ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ᴘʟᴀɴꜱ\n\n"
        "13. **/settings**\n"
        "> 1. setchatid : ᴛᴏ ᴅɪʀᴇᴄᴛʟʏ ᴜᴘʟᴏᴀᴅ ɪɴ ᴄʜᴀɴɴᴇʟ ᴏʀ ɢʀᴏᴜᴘ ᴏʀ ᴜꜱᴇʀ'ꜱ dm ᴜꜱᴇ ɪᴛ ᴡɪᴛʜ -100[chatid]\n"
        "> 2. setrename : ᴛᴏ ᴀᴅᴅ ᴄᴜꜱᴛᴏᴍ ʀᴇɴᴀᴍᴇ ᴛᴀɢ ᴏʀ ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ\n"
        "> 3. caption : ᴛᴏ ᴀᴅᴅ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ\n"
        "> 4. replacewords : ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ꜰᴏʀ ᴡᴏʀᴅꜱ ɪɴ ᴅᴇʟᴇᴛᴇᴅ ꜱᴇᴛ ᴠɪᴀ remove words\n"
        "> 5. reset : ᴛᴏ ʀᴇꜱᴇᴛ ᴛʜɪɴɢꜱ ʙᴀᴄᴋ ᴛᴏ ᴅᴇꜰᴀᴜʟᴛ\n"
        "**__ᴘᴏᴡᴇʀᴇᴅ ʙʏ aman bots__**"
    )
]
 
 
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return
 
    prev_button = InlineKeyboardButton("◀️ ᴘʀᴇᴠɪᴏᴜꜱ", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("ɴᴇxᴛ ▶️", callback_data=f"help_next_{page_number}")
 
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)
 
    keyboard = InlineKeyboardMarkup([buttons])
 
    await message.delete()
 
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )
 
 
@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
 
    await send_or_edit_help_page(client, message, 0)
 
 
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])
 
    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1
 
    await send_or_edit_help_page(client, callback_query.message, page_number)
 
    await callback_query.answer()
 
 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
 
@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "> 📜 **ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ** 📜\n\n"
        "✨ ᴡᴇ ᴀʀᴇ ɴᴏᴛ ʀᴇꜱᴘᴏɴꜱɪʙʟᴇ ꜰᴏʀ ᴜꜱᴇʀ ᴅᴇᴇᴅꜱ, ᴀɴᴅ ᴡᴇ ᴅᴏ ɴᴏᴛ ᴘʀᴏᴍᴏᴛᴇ ᴄᴏᴘʏʀɪɢʜᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ. ɪꜰ ᴀɴʏ ᴜꜱᴇʀ ᴇɴɢᴀɢᴇꜱ ɪɴ ꜱᴜᴄʜ ᴀᴄᴛɪᴏɴꜱ, ɪᴛ ɪꜱ ꜱᴏʟᴇʟʏ ᴛʜᴇɪʀ ʀᴇꜱᴘᴏɴꜱɪʙɪʟɪᴛʏ.\n"
        "✨ __ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ᴀɴᴅ ʙᴀɴɴɪɴɢ ᴏꜰ ᴜꜱᴇʀꜱ ᴀʀᴇ ᴀᴛ ᴏᴜʀ ᴅɪꜱᴄʀᴇᴛɪᴏɴ; ᴡᴇ ʀᴇꜱᴇʀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʙᴀɴ ᴏʀ ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜꜱᴇʀꜱ ᴀᴛ ᴀɴʏ ᴛɪᴍᴇ.__\n"
        "✨ ᴀʟʟ ᴅᴇᴄɪꜱɪᴏɴꜱ ʀᴇɢᴀʀᴅɪɴɢ ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ᴀʀᴇ ᴍᴀᴅᴇ ᴀᴛ ᴏᴜʀ ᴅɪꜱᴄʀᴇᴛɪᴏɴ ᴀɴᴅ ᴍᴏᴏᴅ.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 ꜱᴇᴇ ᴘʟᴀɴꜱ", callback_data="see_plan")],
            [InlineKeyboardButton("💬 ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ", url="https://t.me/amangodz")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)
 
 
@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = (
        "> 💰 **ᴘʀᴇᴍɪᴜᴍ ᴘʀɪᴄᴇ**:\n\n ꜱᴛᴀʀᴛɪɴɢ ꜰʀᴏᴍ $0.5 ᴏʀ 40 inr ᴀᴄᴄᴇᴘᴛᴇᴅ ᴠɪᴀ **__ᴜᴘɪ__** (ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ ᴀᴘᴘʟʏ).\n"
        "📥 **ᴅᴏᴡɴʟᴏᴀᴅ ʟɪᴍɪᴛ**: ᴜꜱᴇʀꜱ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴜᴘ ᴛᴏ 10,000 ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʙᴀᴛᴄʜ ᴄᴏᴍᴍᴀɴᴅ.\n"
        "🛑 **ʙᴀᴛᴄʜ**: ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ /batch ᴄᴏᴍᴍᴀɴᴅ.\n"
        "   - ᴜꜱᴇʀꜱ ᴀʀᴇ ᴀᴅᴠɪꜱᴇᴅ ᴛᴏ ᴡᴀɪᴛ ꜰᴏʀ ᴛʜᴇ ᴘʀᴏᴄᴇꜱꜱ ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴄᴀɴᴄᴇʟ ʙᴇꜰᴏʀᴇ ᴘʀᴏᴄᴇᴇᴅɪɴɢ ᴡɪᴛʜ ᴀɴʏ ᴅᴏᴡɴʟᴏᴀᴅꜱ ᴏʀ ᴜᴘʟᴏᴀᴅꜱ.\n"
        "📜 **ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ**: ꜰᴏʀ ꜰᴜʟʟ ᴅᴇᴛᴀɪʟꜱ, ᴘʟᴇᜀꜱᴇ ꜱᴇɴᴅ /terms.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 ꜱᴇᴇ ᴛᴇʀᴍꜱ", callback_data="see_terms")],
            [InlineKeyboardButton("💬 ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ", url="https://t.me/amangodz")],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "> 💰 **ᴘʀᴇᴍɪᴜᴍ ᴘʀɪᴄᴇ**\n\n ꜱᴛᴀʀᴛɪɴɢ ꜰʀᴏᴍ $0.5 ᴏʀ 40 inr ᴀᴄᴄᴇᴘᴛᴇᴅ ᴠɪᴀ **__ᴜᴘɪ__** (ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ ᴀᴘᴘʟʏ).\n"
        "📥 **ᴅᴏᴡɴʟᴏᴀᴅ ʟɪᴍɪᴛ**: ᴜꜱᴇʀꜱ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴜᴘ ᴛᴏ 10,000 ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʙᴀᴛᴄʜ ᴄᴏᴍᴍᴀɴᴅ.\n"
        "🛑 **ʙᴀᴛᴄʜ**: ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ /batch ᴄᴏᴍᴍᴀɴᴅ.\n"
        "   - ᴜꜱᴇʀꜱ ᴀʀᴇ ᴀᴅᴠɪꜱᴇᴅ ᴛᴏ ᴡᴀɪᴛ ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴄᴀɴᴄᴇʟ ʙᴇꜰᴏʀᴇ ᴘʀᴏᴄᴇᴇᴅɪɴɢ ᴡɪᴛʜ ᴀɴʏ ᴅᴏᴡɴʟᴏᴀᴅꜱ ᴏʀ ᴜᴘʟᴏᴀᴅꜱ.\n"
        "📜 **ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ**: ꜰᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟꜱ, ꜱᴇɴᴅ /terms ᴏʀ ᴄʟɪᴄᴋ ꜱᴇᴇ ᴛᴇʀᴍꜱ👇\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 ꜱᴇᴇ ᴛᴇʀᴍꜱ", callback_data="see_terms")],
            [InlineKeyboardButton("💬 ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ", url="https://t.me/amangodz")],
        ]
    )
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "> 📜 **ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ** 📜\n\n"
        "✨ ᴡᴇ ᴀʀᴇ ɴᴏᴛ ʀᴇꜱᴘᴏɴꜱɪʙʟᴇ ꜰᴏʀ ᴜꜱᴇʀ ᴅᴇᴇᴅꜱ, ᴀɴᴅ ᴡᴇ ᴅᴏ ɴᴏᴛ ᴘʀᴏᴍᴏᴛᴇ ᴄᴏᴘʏʀɪɢʜᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ. ɪꜰ ᴀɴʏ ᴜꜱᴇʀ ᴇɴɢᴀɢᴇꜱ ɪɴ ꜱᴜᴄʜ ᴀᴄᴛɪᴏɴꜱ, ɪᴛ ɪꜱ ꜱᴏʟᴇʟʏ ᴛʜᴇɪʀ ʀᴇꜱᴘᴏɴꜱɪʙɪʟɪᴛʏ.\n"
        "✨ __ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ᴀɴᴅ ʙᴀɴɴɪɴɢ ᴏꜰ ᴜꜱᴇʀꜱ ᴀʀᴇ ᴀᴛ ᴏᴜʀ ᴅɪꜱᴄʀᴇᴛɪᴏɴ; ᴡᴇ ʀᴇꜱᴇʀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʙᴀɴ ᴏʀ ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜꜱᴇʀꜱ ᴀᴛ ᴀɴʏ ᴛɪᴍᴇ.__\n"
        "✨ ᴀʟʟ ᴅᴇᴄɪꜱɪᴏɴꜱ ʀᴇɢᴀʀᴅɪɴɢ ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ᴀʀᴇ ᴍᴀᴅᴇ ᴀᴛ ᴏᴜʀ ᴅɪꜱᴄʀᴇᴛɪᴏɴ ᴀɴᴅ ᴍᴏᴏᴅ.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 ꜱᴇᴇ ᴘʟᴀɴꜱ", callback_data="see_plan")],
            [InlineKeyboardButton("💬 ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ", url="https://t.me/amangodz")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)