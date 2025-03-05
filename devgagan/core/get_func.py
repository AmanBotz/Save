# ---------------------------------------------------
# File Name: get_func.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-02-01
# Version: 2.0.5
# License: MIT License
# Improved logic handles
# ---------------------------------------------------

import asyncio
import time
import gc
import os
import re
from typing import Callable
from devgagan import app
import aiofiles
from devgagan import sex as gf
from telethon.tl.types import DocumentAttributeVideo, Message
from telethon.sessions import StringSession
import pymongo
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid
from pyrogram.enums import MessageMediaType, ParseMode
from devgagan.core.func import *
from pyrogram.errors import RPCError
from pyrogram.types import Message
from config import MONGO_DB as MONGODB_CONNECTION_STRING, LOG_GROUP, OWNER_ID, STRING, API_ID, API_HASH
from devgagan.core.mongo import db as odb
from telethon import TelegramClient, events, Button
from devgagantools import fast_upload

def thumbnail(sender):
    return f'{sender}.jpg' if os.path.exists(f'{sender}.jpg') else None

# MongoDB database name and collection name
DB_NAME = "smart_users"
COLLECTION_NAME = "super_user"

VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv', 'webm', 'mpg', 'mpeg', '3gp', 'ts', 'm4v', 'f4v', 'vob']
DOCUMENT_EXTENSIONS = ['pdf', 'docs']

mongo_app = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_app[DB_NAME]
collection = db[COLLECTION_NAME]

if STRING:
    from devgagan import pro
    print("ᴀᴘᴘ ɪᴍᴘᴏʀᴛᴇᴅ.")
else:
    pro = None
    print("ꜱᴛʀɪɴɢ ɪꜱ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ. 'ᴀᴘᴘ' ɪꜱ ꜱᴇᴛ ᴛᴏ ɴᴏɴᴇ.")
    
async def fetch_upload_method(user_id):
    """ꜰᴇᴛᴄʜ ᴛʜᴇ ᴜꜱᴇʀ'ꜱ ᴘʀᴇꜰᴇʀʀᴇᴅ ᴜᴘʟᴏᴀᴅ ᴍᴇᴛʜᴏᴅ."""
    user_data = collection.find_one({"user_id": user_id})
    return user_data.get("upload_method", "Pyrogram") if user_data else "Pyrogram"

async def format_caption_to_html(caption: str) -> str:
    caption = re.sub(r"^> (.*)", r"<blockquote>\1</blockquote>", caption, flags=re.MULTILINE)
    caption = re.sub(r"```(.*?)```", r"<pre>\1</pre>", caption, flags=re.DOTALL)
    caption = re.sub(r"`(.*?)`", r"<code>\1</code>", caption)
    caption = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", caption)
    caption = re.sub(r"\*(.*?)\*", r"<b>\1</b>", caption)
    caption = re.sub(r"__(.*?)__", r"<i>\1</i>", caption)
    caption = re.sub(r"_(.*?)_", r"<i>\1</i>", caption)
    caption = re.sub(r"~~(.*?)~~", r"<s>\1</s>", caption)
    caption = re.sub(r"\|\|(.*?)\|\|", r"<details>\1</details>", caption)
    caption = re.sub(r"(.*?)(.*?)", r'<a href="\2">\1</a>', caption)
    return caption.strip() if caption else None
    

async def upload_media(sender, target_chat_id, file, caption, edit, topic_id):
    try:
        upload_method = await fetch_upload_method(sender)  # ꜰᴇᴛᴄʜ ᴛʜᴇ ᴜᴘʟᴏᴀᴅ ᴍᴇᴛʜᴏᴅ (Pyrogram ᴏʀ Telethon)
        metadata = video_metadata(file)
        width, height, duration = metadata['width'], metadata['height'], metadata['duration']
        try:
            thumb_path = await screenshot(file, duration, sender)
        except Exception:
            thumb_path = None

        video_formats = {'mp4', 'mkv', 'avi', 'mov'}
        document_formats = {'pdf', 'docx', 'txt', 'epub'}
        image_formats = {'jpg', 'png', 'jpeg'}

        # Pyrogram upload
        if upload_method == "Pyrogram":
            if file.split('.')[-1].lower() in video_formats:
                dm = await app.send_video(
                    chat_id=target_chat_id,
                    video=file,
                    caption=caption,
                    height=height,
                    width=width,
                    duration=duration,
                    thumb=thumb_path,
                    reply_to_message_id=topic_id,
                    parse_mode=ParseMode.MARKDOWN,
                    progress=progress_bar,
                    progress_args=("╭─────────────────────╮\n│      **__ᴘʏʀᴏɢʀᴀᴍ ᴜᴘʟᴏᴀᴅᴇʀ__**\n├─────────────────────", edit, time.time())
                )
                await dm.copy(LOG_GROUP)
                
            elif file.split('.')[-1].lower() in image_formats:
                dm = await app.send_photo(
                    chat_id=target_chat_id,
                    photo=file,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN,
                    progress=progress_bar,
                    reply_to_message_id=topic_id,
                    progress_args=("╭─────────────────────╮\n│      **__ᴘʏʀᴏɢʀᴀᴍ ᴜᴘʟᴏᴀᴅᴇʀ__**\n├─────────────────────", edit, time.time())
                )
                await dm.copy(LOG_GROUP)
            else:
                dm = await app.send_document(
                    chat_id=target_chat_id,
                    document=file,
                    caption=caption,
                    thumb=thumb_path,
                    reply_to_message_id=topic_id,
                    progress=progress_bar,
                    parse_mode=ParseMode.MARKDOWN,
                    progress_args=("╭─────────────────────╮\n│      **__ᴘʏʀᴏɢʀᴀᴍ ᴜᴘʟᴏᴀᴅᴇʀ__**\n├─────────────────────", edit, time.time())
                )
                await asyncio.sleep(2)
                await dm.copy(LOG_GROUP)

        # Telethon upload
        elif upload_method == "Telethon":
            await edit.delete()
            progress_message = await gf.send_message(sender, "**__ᴜᴘʟᴏᴀᴅɪɴɢ...__**")
            caption = await format_caption_to_html(caption)
            uploaded = await fast_upload(
                gf, file,
                reply=progress_message,
                name=None,
                progress_bar_function=lambda done, total: progress_callback(done, total, sender)
            )
            await progress_message.delete()

            attributes = [
                DocumentAttributeVideo(
                    duration=duration,
                    w=width,
                    h=height,
                    supports_streaming=True
                )
            ] if file.split('.')[-1].lower() in video_formats else []

            await gf.send_file(
                target_chat_id,
                uploaded,
                caption=caption,
                attributes=attributes,
                reply_to=topic_id,
                thumb=thumb_path
            )
            await gf.send_file(
                LOG_GROUP,
                uploaded,
                caption=caption,
                attributes=attributes,
                thumb=thumb_path
            )

    except Exception as e:
        await app.send_message(LOG_GROUP, f"**__ᴜᴘʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ:__** {str(e)}")
        print(f"Error during media upload: {e}")

    finally:
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)
        gc.collect()


async def get_msg(userbot, sender, edit_id, msg_link, i, message):
    try:
        # ꜱᴀɴɪᴛɪᴢᴇ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ʟɪɴᴋ
        msg_link = msg_link.split("?single")[0]
        chat, msg_id = None, None
        saved_channel_ids = load_saved_channel_ids()
        size_limit = 2 * 1024 * 1024 * 1024  # 1.99 GB size limit
        file = ''
        edit = ''
        # ᴇxᴛʀᴀᴄᴛ ᴄʜᴀᴛ ᴀɴᴅ ᴍᴇꜱꜱᴀɢᴇ ɪᴅ ꜰᴏʀ ᴠᴀʟɪᴅ ᴛᴇʟᴇɢʀᴀᴍ ʟɪɴᴋꜱ
        if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
            parts = msg_link.split("/")
            if 't.me/b/' in msg_link:
                chat = parts[-2]
                msg_id = int(parts[-1]) + i  # ꜰɪxᴇᴅ ʙᴏᴛ ᴘʀᴏʙʟᴇᴍ 
            else:
                chat = int('-100' + parts[parts.index('c') + 1])
                msg_id = int(parts[-1]) + i

            if chat in saved_channel_ids:
                await app.edit_message_text(
                    message.chat.id, edit_id,
                    "ꜱᴏʀʀʏ! ᴛʜɪꜱ ᴄʜᴀɴɴᴇʟ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ʙʏ **__ᴀᴍᴀɴ ʙᴏᴛꜱ__**."
                )
                return
            
        elif '/s/' in msg_link:  # ꜰɪxᴇᴅ ꜱᴛᴏʀʏ ᴛʏᴘᴏ
            edit = await app.edit_message_text(sender, edit_id, "ꜱᴛᴏʀʏ ʟɪɴᴋ ᴅɪᴄᴛᴇᴄᴛᴇᴅ...")
            if userbot is None:
                await edit.edit("ʟᴏɢɪɴ ɪɴ ʙᴏᴛ ᴛᴏ ꜱᴀᴠᴇ ꜱᴛᴏʀɪᴇꜱ...")
                return
            parts = msg_link.split("/")
            chat = parts[3]
            
            if chat.isdigit():
                chat = f"-100{chat}"
            
            msg_id = int(parts[-1])
            await download_user_stories(userbot, chat, msg_id, edit, sender)
            await edit.delete(2)
            return
        
        else:
            edit = await app.edit_message_text(sender, edit_id, "ᴘᴜʙʟɪᴄ ʟɪɴᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ...")
            chat = msg_link.split("t.me/")[1].split("/")[0]
            msg_id = int(msg_link.split("/")[-1])
            await copy_message_with_chat_id(app, userbot, sender, chat, msg_id, edit)
            await edit.delete(2)
            return
            
        # ꜰᴇᴛᴄʜ ᴛʜᴇ ᴛᴀʀɢᴇᴛ ᴍᴇꜱꜱᴀɢᴇ
        msg = await userbot.get_messages(chat, msg_id)
        if msg.service or msg.empty:
            await app.delete_messages(sender, edit_id)
            return

        target_chat_id = user_chat_ids.get(message.chat.id, message.chat.id)
        topic_id = None
        if '/' in str(target_chat_id):
            target_chat_id, topic_id = map(int, target_chat_id.split('/', 1))

        if msg.media == MessageMediaType.WEB_PAGE_PREVIEW:
            await clone_message(app, msg, target_chat_id, topic_id, edit_id, LOG_GROUP)
            return

        if msg.text:
            await clone_text_message(app, msg, target_chat_id, topic_id, edit_id, LOG_GROUP)
            return

        if msg.sticker:
            await handle_sticker(app, msg, target_chat_id, topic_id, edit_id, LOG_GROUP)
            return

        file_size = get_message_file_size(msg)
        file_name = await get_media_filename(msg)
        edit = await app.edit_message_text(sender, edit_id, "**__ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...__**")

        file = await userbot.download_media(
            msg,
            file_name=file_name,
            progress=progress_bar,
            progress_args=("╭─────────────────────╮\n│      **__ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ__...**\n├─────────────────────", edit, time.time())
        )
        
        caption = await get_final_caption(msg, sender)
        file = await rename_file(file, sender)
        if msg.audio:
            result = await app.send_audio(target_chat_id, file, caption=caption, reply_to_message_id=topic_id)
            await result.copy(LOG_GROUP)
            await edit.delete(2)
            os.remove(file)
            return
        
        if msg.voice:
            result = await app.send_voice(target_chat_id, file, reply_to_message_id=topic_id)
            await result.copy(LOG_GROUP)
            await edit.delete(2)
            os.remove(file)
            return

        if msg.video_note:
            result = await app.send_video_note(target_chat_id, file, reply_to_message_id=topic_id)
            await result.copy(LOG_GROUP)
            await edit.delete(2)
            os.remove(file)
            return

        if msg.photo:
            result = await app.send_photo(target_chat_id, file, caption=caption, reply_to_message_id=topic_id)
            await result.copy(LOG_GROUP)
            await edit.delete(2)
            os.remove(file)
            return

        if file_size > size_limit and (free_check == 1 or pro is None):
            await edit.delete()
            await split_and_upload_file(app, sender, target_chat_id, file, caption, topic_id)
            return
        elif file_size > size_limit:
            await handle_large_file(file, sender, edit, caption)
        else:
            await upload_media(sender, target_chat_id, file, caption, edit, topic_id)

    except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
        await app.edit_message_text(sender, edit_id, "ʜᴀᴠᴇ ʏᴏᴜ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ?")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if file and os.path.exists(file):
            os.remove(file)
        if edit:
            await edit.delete(2)
        
async def clone_message(app, msg, target_chat_id, topic_id, edit_id, log_group):
    edit = await app.edit_message_text(target_chat_id, edit_id, "ᴄʟᴏɴɪɴɢ...")
    devgaganin = await app.send_message(target_chat_id, msg.text.markdown, reply_to_message_id=topic_id)
    await devgaganin.copy(log_group)
    await edit.delete()

async def clone_text_message(app, msg, target_chat_id, topic_id, edit_id, log_group):
    edit = await app.edit_message_text(target_chat_id, edit_id, "ᴄʟᴏɴɪɴɢ ᴛᴇxᴛ ᴍᴇꜱꜱᴀɢᴇ...")
    devgaganin = await app.send_message(target_chat_id, msg.text.markdown, reply_to_message_id=topic_id)
    await devgaganin.copy(log_group)
    await edit.delete()

async def handle_sticker(app, msg, target_chat_id, topic_id, edit_id, log_group):
    edit = await app.edit_message_text(target_chat_id, edit_id, "ʜᴀɴᴅʟɪɴɢ ꜱᴛɪᴄᴋᴇʀ...")
    result = await app.send_sticker(target_chat_id, msg.sticker.file_id, reply_to_message_id=topic_id)
    await result.copy(log_group)
    await edit.delete()

async def get_media_filename(msg):
    if msg.document:
        return msg.document.file_name
    if msg.video:
        return msg.video.file_name if msg.video.file_name else "temp.mp4"
    if msg.photo:
        return "temp.jpg"
    return "unknown_file"

def get_message_file_size(msg):
    if msg.document:
        return msg.document.file_size
    if msg.photo:
        return msg.photo.file_size
    if msg.video:
        return msg.video.file_size
    return 1

async def get_final_caption(msg, sender):
    if msg.caption:
        original_caption = msg.caption.markdown
    else:
        original_caption = ""
    
    custom_caption = get_user_caption_preference(sender)
    final_caption = format_caption(original_caption, sender, custom_caption)
    
    return final_caption if final_caption else None


async def download_user_stories(userbot, chat_id, msg_id, edit, sender):
    try:
        story = await userbot.get_stories(chat_id, msg_id)
        if not story:
            await edit.edit("ɴᴏ ꜱᴛᴏʀʏ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ ᴛʜɪꜱ ᴜꜱᴇʀ.")
            return  
        if not story.media:
            await edit.edit("ᴛʜᴇ ꜱᴛᴏʀʏ ᴅᴏᴇꜱɴ'ᴛ ᴄᴏɴᴛᴀɪɴ ᴀɴʏ ᴍᴇᴅɪᴀ.")
            return
        await edit.edit("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜱᴛᴏʀʏ...")
        file_path = await userbot.download_media(story)
        print(f"Story downloaded: {file_path}")
        if story.media:
            await edit.edit("ᴜᴘʟᴏᴀᴅɪɴɢ ꜱᴛᴏʀʏ...")
            if story.media == MessageMediaType.VIDEO:
                await app.send_video(sender, file_path)
            elif story.media == MessageMediaType.DOCUMENT:
                await app.send_document(sender, file_path)
            elif story.media == MessageMediaType.PHOTO:
                await app.send_photo(sender, file_path)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)  
        await edit.edit("ꜱᴛᴏʀʏ ᴘʀᴏᴄᴇꜱꜱᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.")
    except RPCError as e:
        print(f"Failed to fetch story: {e}")
        await edit.edit(f"ᴇʀʀᴏʀ: {e}")
        
async def copy_message_with_chat_id(app, userbot, sender, chat_id, message_id, edit):
    target_chat_id = user_chat_ids.get(sender, sender)
    file = None
    result = None
    size_limit = 2 * 1024 * 1024 * 1024  # 2 GB size limit

    try:
        msg = await app.get_messages(chat_id, message_id)
        custom_caption = get_user_caption_preference(sender)
        final_caption = format_caption(msg.caption.markdown if msg.caption else "", sender, custom_caption)

        topic_id = None
        if '/' in str(target_chat_id):
            target_chat_id, topic_id = map(int, target_chat_id.split('/', 1))

        if msg.media:
            result = await send_media_message(app, target_chat_id, msg, final_caption, topic_id)
            return
        elif msg.text:
            result = await app.copy_message(target_chat_id, chat_id, message_id, reply_to_message_id=topic_id)
            return

        if result is None:
            await edit.edit("ᴛʀʏɪɴɢ ɪꜰ ɪᴛ ɪꜱ ᴀ ɢʀᴏᴜᴘ...")
            try:
                await userbot.join_chat(chat_id)
            except Exception as e:
                print(e)
                pass
            chat_id = (await userbot.get_chat(f"@{chat_id}")).id
            msg = await userbot.get_messages(chat_id, message_id)

            if not msg or msg.service or msg.empty:
                return

            if msg.text:
                await app.send_message(target_chat_id, msg.text.markdown, reply_to_message_id=topic_id)
                return

            final_caption = format_caption(msg.caption.markdown if msg.caption else "", sender, custom_caption)
            file = await userbot.download_media(
                msg,
                progress=progress_bar,
                progress_args=("╭─────────────────────╮\n│      **__ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ__...**\n├─────────────────────", edit, time.time())
            )
            file = await rename_file(file, sender)

            if msg.photo:
                result = await app.send_photo(target_chat_id, file, caption=final_caption, reply_to_message_id=topic_id)
            elif msg.video or msg.document:
                freecheck = await chk_user(chat_id, sender)
                file_size = get_message_file_size(msg)
                if file_size > size_limit and (freecheck == 1 or pro is None):
                    await edit.delete()
                    await split_and_upload_file(app, sender, target_chat_id, file, caption, topic_id)
                    return       
                elif file_size > size_limit:
                    await handle_large_file(file, sender, edit, final_caption)
                    return
                await upload_media(sender, target_chat_id, file, final_caption, edit, topic_id)
            elif msg.audio:
                result = await app.send_audio(target_chat_id, file, caption=final_caption, reply_to_message_id=topic_id)
            elif msg.voice:
                result = await app.send_voice(target_chat_id, file, reply_to_message_id=topic_id)
            elif msg.sticker:
                result = await app.send_sticker(target_chat_id, msg.sticker.file_id, reply_to_message_id=topic_id)
            else:
                await edit.edit("ᴜɴꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ.")

    except Exception as e:
        print(f"Error : {e}")
        pass

    finally:
        if file and os.path.exists(file):
            os.remove(file)


async def send_media_message(app, target_chat_id, msg, caption, topic_id):
    try:
        if msg.video:
            return await app.send_video(target_chat_id, msg.video.file_id, caption=caption, reply_to_message_id=topic_id)
        if msg.document:
            return await app.send_document(target_chat_id, msg.document.file_id, caption=caption, reply_to_message_id=topic_id)
        if msg.photo:
            return await app.send_photo(target_chat_id, msg.photo.file_id, caption=caption, reply_to_message_id=topic_id)
    except Exception as e:
        print(f"Error while sending media: {e}")
    
    return await app.copy_message(target_chat_id, msg.chat.id, msg.id, reply_to_message_id=topic_id)
    

def format_caption(original_caption, sender, custom_caption):
    delete_words = load_delete_words(sender)
    replacements = load_replacement_words(sender)

    for word in delete_words:
        original_caption = original_caption.replace(word, '  ')
    for word, replace_word in replacements.items():
        original_caption = original_caption.replace(word, replace_word)

    return f"{original_caption}\n\n__**{custom_caption}**__" if custom_caption else original_caption

# ------------------------ Button Mode Editz FOR SETTINGS ----------------------------

user_chat_ids = {}

def load_user_data(user_id, key, default_value=None):
    try:
        user_data = collection.find_one({"_id": user_id})
        return user_data.get(key, default_value) if user_data else default_value
    except Exception as e:
        print(f"Error loading {key}: {e}")
        return default_value

def load_saved_channel_ids():
    saved_channel_ids = set()
    try:
        for channel_doc in collection.find({"channel_id": {"$exists": True}}):
            saved_channel_ids.add(channel_doc["channel_id"])
    except Exception as e:
        print(f"Error loading saved channel IDs: {e}")
    return saved_channel_ids

def save_user_data(user_id, key, value):
    try:
        collection.update_one(
            {"_id": user_id},
            {"$set": {key: value}},
            upsert=True
        )
    except Exception as e:
        print(f"Error saving {key}: {e}")

load_delete_words = lambda user_id: set(load_user_data(user_id, "delete_words", []))
save_delete_words = lambda user_id, words: save_user_data(user_id, "delete_words", list(words))

load_replacement_words = lambda user_id: load_user_data(user_id, "replacement_words", {})
save_replacement_words = lambda user_id, replacements: save_user_data(user_id, "replacement_words", replacements)

def load_user_session(user_id):
    return load_user_data(user_id, "session")

set_dupload = lambda user_id, value: save_user_data(user_id, "dupload", value)
get_dupload = lambda user_id: load_user_data(user_id, "dupload", False)

user_rename_preferences = {}
user_caption_preferences = {}

async def set_rename_command(user_id, custom_rename_tag):
    user_rename_preferences[str(user_id)] = custom_rename_tag

get_user_rename_preference = lambda user_id: user_rename_preferences.get(str(user_id), '')

async def set_caption_command(user_id, custom_caption):
    user_caption_preferences[str(user_id)] = custom_caption

get_user_caption_preference = lambda user_id: user_caption_preferences.get(str(user_id), '')

sessions = {}
m = None
SET_PIC = "settings.jpg"
MESS = "ᴄᴜꜱᴛᴏᴍɪᴢᴇ ʙʏ ʏᴏᴜʀ ᴇɴᴅ ᴀɴᴅ ᴄᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ꜱᴇᴛᴛɪɴɢꜱ ..."

@gf.on(events.NewMessage(incoming=True, pattern='/settings'))
async def settings_command(event):
    user_id = event.sender_id
    await send_settings_message(event.chat.id, user_id)

async def send_settings_message(chat_id, user_id):
    buttons = [
        [Button.inline("Set Chat ID", b'setchat'), Button.inline("Set Rename Tag", b'setrename')],
        [Button.inline("Caption", b'setcaption'), Button.inline("Replace Words", b'setreplacement')],
        [Button.inline("Remove Words", b'delete'), Button.inline("Reset", b'reset')],
        [Button.inline("Logout", b'logout')],
        [Button.inline("Set Thumbnail", b'setthumb'), Button.inline("Remove Thumbnail", b'remthumb')],
        [Button.url("Report Errors", "https://t.me/amangodz")]
    ]
    await gf.send_file(
        chat_id,
        file=SET_PIC,
        caption=MESS,
        buttons=buttons
    )

pending_photos = {}

@gf.on(events.CallbackQuery)
async def callback_query_handler(event):
    user_id = event.sender_id
    
    if event.data == b'setchat':
        await event.respond("ꜱᴇɴᴅ ᴍᴇ ᴛʜᴇ ɪᴅ ᴏꜰ ᴛʜᴀᴛ ᴄʜᴀᴛ:")
        sessions[user_id] = 'setchat'

    elif event.data == b'setrename':
        await event.respond("ꜱᴇɴᴅ ᴍᴇ ᴛʜᴇ ʀᴇɴᴀᴍᴇ ᴛᴀɢ:")
        sessions[user_id] = 'setrename'
    
    elif event.data == b'setcaption':
        await event.respond("ꜱᴇɴᴅ ᴍᴇ ᴛʜᴇ ᴄᴀᴘᴛɪᴏɴ:")
        sessions[user_id] = 'setcaption'

    elif event.data == b'setreplacement':
        await event.respond("ꜱᴇɴᴅ ᴍᴇ ᴛʜᴇ ʀᴇᴘʟᴀᴄᴇᴍᴇɴᴛ ᴡᴏʀᴅꜱ ɪɴ ᴛʜᴇ ꜰᴏʀᴍᴀᴛ: 'WORD(s)' 'REPLACEWORD'")
        sessions[user_id] = 'setreplacement'

    elif event.data == b'addsession':
        await event.respond("ꜱᴇɴᴅ ᴘʏʀᴏɢʀᴀᴍ V2 ꜱᴇꜱꜱɪᴏɴ")
        sessions[user_id] = 'addsession'

    elif event.data == b'delete':
        await event.respond("ꜱᴇɴᴅ ᴡᴏʀᴅꜱ ꜱᴇᴘᴇʀᴀᴛᴇᴅ ʙʏ ꜱᴘᴀᴄᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛʜᴇᴍ ғʀᴏᴍ ᴄᴀᴘᴛɪᴏɴ ...")
        sessions[user_id] = 'deleteword'
        
    elif event.data == b'logout':
        await odb.remove_session(user_id)
        user_data = await odb.get_data(user_id)
        if user_data and user_data.get("session") is None:
            await event.respond("ʟᴏɢɢᴇᴅ ᴏᴜᴛ ᴀɴᴅ ᴅᴇʟᴇᴛᴇᴅ ꜱᴇꜱꜱɪᴏɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.")
        else:
            await event.respond("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʟᴏɢɢᴇᴅ ɪɴ.")
        
    elif event.data == b'setthumb':
        pending_photos[user_id] = True
        await event.respond("ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴛʜᴇ ᴘʜᴏᴛᴏ ᴡɪᴛʜ ᴛʜᴇ ᴛʜᴜᴍʙɴᴀɪʟ.")
    
    elif event.data == b'pdfwt':
        await event.respond("ᴡᴀᴛᴇʀᴍᴀʀᴋ ɪꜱ ᴘʀᴏ+ ᴘʟᴀɴ.. ᴄᴏɴᴛᴀᴄᴛ @amangodz")
        return

    elif event.data == b'uploadmethod':
        user_data = collection.find_one({'user_id': user_id})
        current_method = user_data.get('upload_method', 'Pyrogram') if user_data else 'Pyrogram'
        pyrogram_check = " ✅" if current_method == "Pyrogram" else ""
        telethon_check = " ✅" if current_method == "Telethon" else ""
        buttons = [
            [Button.inline(f"Pyrogram v2{pyrogram_check}", b'pyrogram')],
            [Button.inline(f"SpyLib v1 ⚡{telethon_check}", b'telethon')]
        ]
        await event.edit("ᴄʜᴏᴏꜱᴇ ʏᴏᴜʀ ᴘʀᴇꜰᴇʀʀᴇᴅ ᴜᴘʟᴏᴀᴅ ᴍᴇᴛʜᴏᴅ:\n\n__**ɴᴏᴛᴇ: ꜱᴘʏʟɪʙ ⚡, ʙᴜɪʟᴛ ᴏɴ ᴛᴇʟᴇᴛʜᴏɴ (ʙᴀꜱᴇ), ʙᴛɪʟʟ ɪɴ ʙᴇᴛᴀ.__**", buttons=buttons)

    elif event.data == b'pyrogram':
        save_user_upload_method(user_id, "Pyrogram")
        await event.edit("ᴜᴘʟᴏᴀᴅ ᴍᴇᴛʜᴏᴅ ꜱᴇᴛ ᴛᴏ **ᴘʏʀᴏɢʀᴀᴍ** ✅")

    elif event.data == b'telethon':
        save_user_upload_method(user_id, "Telethon")
        await event.edit("ᴜᴘʟᴏᴀᴅ ᴍᴇᴛʜᴏᴅ ꜱᴇᴛ ᴛᴏ **ꜱᴘʏʟɪʙ ⚡\n\nᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴄʜᴏᴏꜱɪɴɢ ᴛʜɪꜱ ʟɪʙʀᴀʀʏ.** ✅")        
        
    elif event.data == b'reset':
        try:
            user_id_str = str(user_id)
            collection.update_one(
                {"_id": user_id},
                {"$unset": {
                    "delete_words": "",
                    "replacement_words": "",
                    "watermark_text": "",
                    "duration_limit": ""
                }}
            )
            collection.update_one(
                {"user_id": user_id},
                {"$unset": {
                    "delete_words": "",
                    "replacement_words": "",
                    "watermark_text": "",
                    "duration_limit": ""
                }}
            )            
            user_chat_ids.pop(user_id, None)
            user_rename_preferences.pop(user_id_str, None)
            user_caption_preferences.pop(user_id_str, None)
            thumbnail_path = f"{user_id}.jpg"
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            await event.respond("✅ ʀᴇꜱᴇᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ, ᴛᴏ ʟᴏɢᴏᴜᴛ ᴄʟɪᴄᴋ /logout")
        except Exception as e:
            await event.respond(f"ᴇʀʀᴏʀ ᴄʟᴇᴀʀɪɴɢ ᴅᴇʟᴇᴛᴇ ʟɪꜱᴛ: {e}")
    
    elif event.data == b'remthumb':
        try:
            os.remove(f'{user_id}.jpg')
            await event.respond("ᴛʜᴜᴍʙɴᴀɪʟ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!")
        except FileNotFoundError:
            await event.respond("ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ ꜰᴏᴜɴᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ.")
    

@gf.on(events.NewMessage(func=lambda e: e.sender_id in pending_photos))
async def save_thumbnail(event):
    user_id = event.sender_id
    if event.photo:
        temp_path = await event.download_media()
        if os.path.exists(f'{user_id}.jpg'):
            os.remove(f'{user_id}.jpg')
        os.rename(temp_path, f'./{user_id}.jpg')
        await event.respond("ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴀᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!")
    else:
        await event.respond("ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ... ʀᴇᴛʀʏ")
    pending_photos.pop(user_id, None)

def save_user_upload_method(user_id, method):
    collection.update_one(
        {'user_id': user_id},
        {'$set': {'upload_method': method}},
        upsert=True
    )

@gf.on(events.NewMessage)
async def handle_user_input(event):
    user_id = event.sender_id
    if user_id in sessions:
        session_type = sessions[user_id]

        if session_type == 'setchat':
            try:
                chat_id = event.text
                user_chat_ids[user_id] = chat_id
                await event.respond("ᴄʜᴀᴛ ɪᴅ ꜱᴇᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!")
            except ValueError:
                await event.respond("ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ!")
                
        elif session_type == 'setrename':
            custom_rename_tag = event.text
            await set_rename_command(user_id, custom_rename_tag)
            await event.respond(f"ᴄᴜꜱᴛᴏᴍ ʀᴇɴᴀᴍᴇ ᴛᴀɢ ꜱᴇᴛ ᴛᴏ: {custom_rename_tag}")
        
        elif session_type == 'setcaption':
            custom_caption = event.text
            await set_caption_command(user_id, custom_caption)
            await event.respond(f"ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ꜱᴇᴛ ᴛᴏ: {custom_caption}")

        elif session_type == 'setreplacement':
            match = re.match(r"'(.+)' '(.+)'", event.text)
            if not match:
                await event.respond("ᴜꜱᴀɢᴇ: 'WORD(s)' 'REPLACEWORD'")
            else:
                word, replace_word = match.groups()
                delete_words = load_delete_words(user_id)
                if word in delete_words:
                    await event.respond(f"ᴛʜᴇ ᴡᴏʀᴅ '{word}' ɪꜱ ɪɴ ᴛʜᴇ ᴅᴇʟᴇᴛᴇ ꜱᴇᴛ ᴀɴᴅ ᴄᴀɴɴᴏᴛ ʙᴇ ʀᴇᴘʟᴀᴄᴇᴅ.")
                else:
                    replacements = load_replacement_words(user_id)
                    replacements[word] = replace_word
                    save_replacement_words(user_id, replacements)
                    await event.respond(f"ʀᴇᴘʟᴀᴄᴇᴍᴇɴᴛ ꜱᴀᴠᴇᴅ: '{word}' ᴡɪʟʟ ʙᴇ ʀᴇᴘʟᴀᴄᴇᴅ ᴡɪᴛʜ '{replace_word}'")
        elif session_type == 'addsession':
            session_string = event.text
            await odb.set_session(user_id, session_string)
            await event.respond("✅ ꜱᴇꜱꜱɪᴏɴ ꜱᴛʀɪɴɢ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!")
                
        elif session_type == 'deleteword':
            words_to_delete = event.message.text.split()
            delete_words = load_delete_words(user_id)
            delete_words.update(words_to_delete)
            save_delete_words(user_id, delete_words)
            await event.respond(f"ᴡᴏʀᴅꜱ ᴀᴅᴅᴇᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʟɪꜱᴛ: {', '.join(words_to_delete)}")
            
        del sessions[user_id]
    
@gf.on(events.NewMessage(incoming=True, pattern='/lock'))
async def lock_command_handler(event):
    if event.sender_id not in OWNER_ID:
        return await event.respond("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")
    
    try:
        channel_id = int(event.text.split(' ')[1])
    except (ValueError, IndexError):
        return await event.respond("ɪɴᴠᴀʟɪᴅ /ʟᴏᴄᴋ ᴄᴏᴍᴍᴀɴᴅ. ᴜꜱᴇ /ʟᴏᴄᴋ ᴄʜᴀɴɴᴇʟ_ɪᴅ.")
    
    try:
        collection.insert_one({"channel_id": channel_id})
        await event.respond(f"ᴄʜᴀɴɴᴇʟ ɪᴅ {channel_id} ʟᴏᴄᴋᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.")
    except Exception as e:
        await event.respond(f"ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ʟᴏᴄᴋɪɴɢ ᴄʜᴀɴɴᴇʟ ɪᴅ: {str(e)}")


async def handle_large_file(file, sender, edit, caption):
    if pro is None:
        await edit.edit("**__ 4ɢʙ ᴛʀɪɢɢᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ __**")
        os.remove(file)
        gc.collect()
        return
    
    dm = None
    print("4ɢʙ ᴛʀɪɢɢᴇʀ ꜰᴏᴜɴᴅ.")
    await edit.edit("**__ 4ɢʙ ᴛʀɪɢɢᴇʀ ᴄᴏɴɴᴇᴄᴛᴇᴅ... __**\n\n")
    target_chat_id = user_chat_ids.get(sender, sender)
    file_extension = str(file).split('.')[-1].lower()
    metadata = video_metadata(file)
    duration = metadata['duration']
    width = metadata['width']
    height = metadata['height']
    try:
        thumb_path = await screenshot(file, duration, sender)
    except Exception:
        thumb_path = None
    try:
        if file_extension in VIDEO_EXTENSIONS:
            dm = await pro.send_video(
                LOG_GROUP,
                video=file,
                caption=caption,
                thumb=thumb_path,
                height=height,
                width=width,
                duration=duration,
                progress=progress_bar,
                progress_args=(
                    "╭─────────────────────╮\n│       **__4ɢʙ ᴜᴘʟᴏᴀᴅᴇʀ ⚡__**\n├─────────────────────",
                    edit,
                    time.time()
                )
            )
        else:
            dm = await pro.send_document(
                LOG_GROUP,
                document=file,
                caption=caption,
                thumb=thumb_path,
                progress=progress_bar,
                progress_args=(
                    "╭─────────────────────╮\n│      **__4ɢʙ ᴜᴘʟᴏᴀᴅᴇʀ ⚡__**\n├─────────────────────",
                    edit,
                    time.time()
                )
            )

        from_chat = dm.chat.id
        msg_id = dm.id
        freecheck = 0
        if freecheck == 1:
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("💎 ɢᴇᴛ ᴘʀᴏᴍɪᴜᴍ ᴛᴏ ꜰᴏʀᴡᴀʀᴅ", url="https://t.me/amangodz")]
                ]
            )
            await app.copy_message(
                target_chat_id,
                from_chat,
                msg_id,
                protect_content=True,
                reply_markup=reply_markup
            )
        else:
            await app.copy_message(
                target_chat_id,
                from_chat,
                msg_id
            )
            
    except Exception as e:
        print(f"Error while sending file: {e}")

    finally:
        await edit.delete()
        os.remove(file)
        gc.collect()
        return

async def rename_file(file, sender):
    delete_words = load_delete_words(sender)
    custom_rename_tag = get_user_rename_preference(sender)
    replacements = load_replacement_words(sender)
    
    last_dot_index = str(file).rfind('.')
    
    if last_dot_index != -1 and last_dot_index != 0:
        ggn_ext = str(file)[last_dot_index + 1:]
        
        if ggn_ext.isalpha() and len(ggn_ext) <= 9:
            if ggn_ext.lower() in VIDEO_EXTENSIONS:
                original_file_name = str(file)[:last_dot_index]
                file_extension = 'mp4'
            else:
                original_file_name = str(file)[:last_dot_index]
                file_extension = ggn_ext
        else:
            original_file_name = str(file)[:last_dot_index]
            file_extension = 'mp4'
    else:
        original_file_name = str(file)
        file_extension = 'mp4'
        
    for word in delete_words:
        original_file_name = original_file_name.replace(word, "")
    for word, replace_word in replacements.items():
        original_file_name = original_file_name.replace(word, replace_word)

    new_file_name = f"{original_file_name} {custom_rename_tag}.{file_extension}"
    await asyncio.to_thread(os.rename, file, new_file_name)
    return new_file_name

async def sanitize(file_name: str) -> str:
    sanitized_name = re.sub(r'[\\/:"*?<>|]', '_', file_name)
    return sanitized_name.strip()
    
async def is_file_size_exceeding(file_path, size_limit):
    try:
        return os.path.getsize(file_path) > size_limit
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except Exception as e:
        print(f"Error while checking file size: {e}")
        return False

user_progress = {}

def progress_callback(done, total, user_id):
    if user_id not in user_progress:
        user_progress[user_id] = {
            'previous_done': 0,
            'previous_time': time.time()
        }
    user_data = user_progress[user_id]
    percent = (done / total) * 100
    completed_blocks = int(percent // 10)
    remaining_blocks = 10 - completed_blocks
    progress_bar = "♦" * completed_blocks + "◇" * remaining_blocks
    done_mb = done / (1024 * 1024)
    total_mb = total / (1024 * 1024)
    speed = done - user_data['previous_done']
    elapsed_time = time.time() - user_data['previous_time']
    if elapsed_time > 0:
        speed_bps = speed / elapsed_time
        speed_mbps = (speed_bps * 8) / (1024 * 1024)
    else:
        speed_mbps = 0
    if speed_bps > 0:
        remaining_time = (total - done) / speed_bps
    else:
        remaining_time = 0
    remaining_time_min = remaining_time / 60
    final = (
        f"╭──────────────────╮\n"
        f"│     **__ꜱᴘʏʟɪʙ ⚡ ᴜᴘʟᴏᴀᴅᴇʀ__**       \n"
        f"├──────────\n"
        f"│ {progress_bar}\n\n"
        f"│ **__ᴘʀᴏɢʀᴇꜱꜱ:__** {percent:.2f}%\n"
        f"│ **__ᴅᴏɴᴇ:__** {done_mb:.2f} MB / {total_mb:.2f} MB\n"
        f"│ **__ꜱᴘᴇᴇᴅ:__** {speed_mbps:.2f} Mbps\n"
        f"│ **__ᴇᴛᴀ:__** {remaining_time_min:.2f} min\n"
        f"╰──────────────────╯\n\n"
        f"**__ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴍᴀɴ ʙᴏᴛꜱ__**"
    )
    user_data['previous_done'] = done
    user_data['previous_time'] = time.time()
    return final

def dl_progress_callback(done, total, user_id):
    if user_id not in user_progress:
        user_progress[user_id] = {
            'previous_done': 0,
            'previous_time': time.time()
        }
    user_data = user_progress[user_id]
    percent = (done / total) * 100
    completed_blocks = int(percent // 10)
    remaining_blocks = 10 - completed_blocks
    progress_bar = "♦" * completed_blocks + "◇" * remaining_blocks
    done_mb = done / (1024 * 1024)
    total_mb = total / (1024 * 1024)
    speed = done - user_data['previous_done']
    elapsed_time = time.time() - user_data['previous_time']
    if elapsed_time > 0:
        speed_bps = speed / elapsed_time
        speed_mbps = (speed_bps * 8) / (1024 * 1024)
    else:
        speed_mbps = 0
    if speed_bps > 0:
        remaining_time = (total - done) / speed_bps
    else:
        remaining_time = 0
    remaining_time_min = remaining_time / 60
    final = (
        f"╭──────────────────╮\n"
        f"│     **__ꜱᴘʏʟɪʙ ⚡ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ__**       \n"
        f"├──────────\n"
        f"│ {progress_bar}\n\n"
        f"│ **__ᴘʀᴏɢʀᴇꜱꜱ:__** {percent:.2f}%\n"
        f"│ **__ᴅᴏɴᴇ:__** {done_mb:.2f} MB / {total_mb:.2f} MB\n"
        f"│ **__ꜱᴘᴇᴇᴅ:__** {speed_mbps:.2f} Mbps\n"
        f"│ **__ᴇᴛᴀ:__** {remaining_time_min:.2f} min\n"
        f"╰──────────────────╯\n\n"
        f"**__ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴍᴀɴ ʙᴏᴛꜱ__**"
    )
    user_data['previous_done'] = done
    user_data['previous_time'] = time.time()
    return final

async def split_and_upload_file(app, sender, target_chat_id, file_path, caption, topic_id):
    if not os.path.exists(file_path):
        await app.send_message(sender, "❌ ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ!")
        return

    file_size = os.path.getsize(file_path)
    start = await app.send_message(sender, f"ℹ️ ꜰɪʟᴇ ꜱɪᴢᴇ: {file_size / (1024 * 1024):.2f} ᴍʙ")
    PART_SIZE =  1.9 * 1024 * 1024 * 1024

    part_number = 0
    async with aiofiles.open(file_path, mode="rb") as f:
        while True:
            chunk = await f.read(PART_SIZE)
            if not chunk:
                break

            base_name, file_ext = os.path.splitext(file_path)
            part_file = f"{base_name}.part{str(part_number).zfill(3)}{file_ext}"

            async with aiofiles.open(part_file, mode="wb") as part_f:
                await part_f.write(chunk)

            edit = await app.send_message(target_chat_id, f"⬆️ ᴜᴘʟᴏᴀᴅɪɴɢ ᴘᴀʀᴛ {part_number + 1}...")
            part_caption = f"{caption} \n\n**Part : {part_number + 1}**"
            await app.send_document(target_chat_id, document=part_file, caption=part_caption, reply_to_message_id=topic_id,
                progress=progress_bar,
                progress_args=("╭─────────────────────╮\n│      **__ᴘʏʀᴏ ᴜᴘʟᴏᴀᴅᴇʀ__**\n├─────────────────────", edit, time.time())
            )
            await edit.delete()
            os.remove(part_file)
            part_number += 1

    await start.delete()
    os.remove(file_path)