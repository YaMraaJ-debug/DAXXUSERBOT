from .. import *
from ..modules.func import *
from ..modules.utils import *

from pyrogram import *
from pytgcalls import StreamType
from pytgcalls.types.input_stream import *
from pytgcalls.types.input_stream.quality import *


# Audio Stream
@app.on_message(commandz(["ply", "play"]) & SUDOERS)
async def audio_stream(client, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    audio = (
        (replied.audio or replied.voice or
        replied.video or replied.document)
        if replied else None
    )
    m = await eor(message, "**🔄 Processing ...**")
    try:
        if audio:
            await m.edit("**📥 Downloading ...**")
            file = await replied.download()
        else:
            if len(message.command) < 2:
                 return await m.edit("**🤖 Give Some Query ...**")
            text = message.text.split(None, 1)[1]
            query = text.split("?si")[0] if "?si=" in text else text
            await m.edit("**🔍 Searching ...**")
            search = get_youtube_video(query)
            stream = search[0]
            file = await get_youtube_stream(stream)
        await m.edit("**🔄 Processing ...**")
        if check := db.get(chat_id):
            pos = await put_que(chat_id, file, "Audio")
            await m.edit(f"**😋 Added To Queue #{pos}**")
        else:
            await call.join_group_call(
                chat_id,
                AudioPiped(
                    file,
                    HighQualityAudio(),
                ),
                stream_type=StreamType().pulse_stream
            )
            await put_que(chat_id, file, "Audio")
            await m.edit("**🥳 Streaming Started!**")
        await m.delete()
    except Exception as e:
        await m.edit(f"**Error:** `{e}`")

  
# Video Stream
@app.on_message(commandz(["vply", "vplay"]) & SUDOERS)
async def video_stream(client, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    video = (
        (replied.audio or replied.voice or
        replied.video or replied.document)
        if replied else None
    )
    m = await eor(message, "**🔄 Processing ...**")
    try:
        if video:
            await m.edit("**📥 Downloading ...**")
            file = await replied.download()
        else:
            if len(message.command) < 2:
                 return await m.edit("**🤖 Give Some Query ...**")
            text = message.text.split(None, 1)[1]
            query = text.split("?si")[0] if "?si=" in text else text
            await m.edit("**🔍 Searching ...**")
            search = get_youtube_video(query)
            stream = search[0]
            file = await get_youtube_stream(stream)
        await m.edit("**🔄 Processing ...**")
        if check := db.get(chat_id):
            pos = await put_que(chat_id, file, "Video")
            await m.edit(f"**😋 Added To Queue #{pos}**")
            await m.delete()
        else:
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(
                    file,
                    HighQualityAudio(),
                    HighQualityVideo(),
                ),
                stream_type=StreamType().pulse_stream
            )
            await put_que(chat_id, file, "Video")
            await m.edit("**🥳 Streaming Started!**")
            await message.delete()
    except Exception as e:
        await m.edit(f"**Error:** `{e}`")


# Pause Stream
@app.on_message(commandz(["pse", "pause"]) & SUDOERS)
async def pause_stream(client, message):
    chat_id = message.chat.id
    try:
        if check := db.get(chat_id):
            await call.pause_stream(chat_id)
            return await eor(message, "**Stream Paused !**")
        else:
            return await eor(message, "**Nothing Playing !**")
    except Exception as e:
        await eor(message, f"**Error:** `{e}`")


# Resume Stream
@app.on_message(commandz(["rsm", "resume"]) & SUDOERS)
async def resume_streams(client, message):
    chat_id = message.chat.id
    try:
        if check := db.get(chat_id):
            await call.resume_stream(chat_id)
            return await eor(message, "**Stream Resumed !**")
        else:
            return await eor(message, "**Nothing Playing !**")
    except Exception as e:
        await eor(message, f"**Error:** `{e}`")
        
        
# Skip To Next Stream
@app.on_message(commandz(["skp", "skip"]) & SUDOERS)
async def change_streams(client, message):
    chat_id = message.chat.id
    try:
        if not (check := db.get(chat_id)):
            return await eor(message, "**Nothing Playing ...**")
        que = db[chat_id]
        que.pop(0)
        if len(que) == 0:
            await call.leave_group_call(chat_id)
            return await eor(message, "Empty Queue !")
        else:
            file = check[0]["file"]
            type = check[0]["type"]
            if type == "Audio":
                stream = AudioPiped(
                    file,
                    HighQualityAudio(),
                )
            elif type == "Video":
                stream = AudioVideoPiped(
                    file,
                    HighQualityAudio(),
                    HighQualityVideo(),
                )
            await call.change_stream(chat_id, stream)
            return await eor(message, "🥳 Skipped !")
    except Exception as e:
        await eor(message, f"**Error:** `{e}`")


# Stop/End Stream
@app.on_message(commandz(["stp", "stop", "end"]) & SUDOERS)
async def leave_streams(client, message):
    chat_id = message.chat.id
    try:
        if check := db.get(chat_id):
            check.pop(0)
            await call.leave_group_call(chat_id)
            return await eor(message, "**Stream Stopped !**")
        else:
            return await eor(message, "**Nothing Playing !**")
    except Exception as e:
        await eor(message, f"**Error:** `{e}`")


__NAME__ = "Vcbot"
__MENU__ = """
**🥀 Audio & Video Player Only
For Telegram Groups 🦋...**

**🌿 Vcbot All Commands:**
`.play` [name] - Play An Audio
Song By Giving Name.

`.vplay` [name] - Play An Video
Song By Giving Name.

`.pause` - To Pause Stream.
`.resume` - To Resume Stream.
`.skip` - Skip To Next Song.
`.end` - To Stop Stream.

**🌷 Vcbot Shortcut Commands:**
=> [ply, vply, pse, rsm, skp, stp]
"""
