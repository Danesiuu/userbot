import asyncio
from random import shuffle

from pyrogram import filters
from pyrogram.types import Message

from PyroUbot import *
from PyroUbot.config import *
from PyroUbot import eor

__MODULE__ = "tagall"
__HELP__ = f"""
 Document for Tagall

• Command: <code>{[0]}tagall</code> [type message/reply message]
• Function: Untuk memention semua anggota grup dengan pesan yang anda inginkan.

• Command: <code>{[0]}batal</code>
• Function: Untuk membatalkan memention anggota grup.
"""


tagallgcid = []


@PY.UBOT("tagall", "batal")
async def _(client, message: Message):
    if message.command[0] == "tagall":
        if message.chat.id in tagallgcid:
            return
        tagallgcid.append(message.chat.id)
        text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else ""
        users = [
            member.user.mention
            async for member in message.chat.get_members()
            if not (member.user.is_bot or member.user.is_deleted)
        ]
        shuffle(users)
        m = message.reply_to_message or message
        for output in [users[i : i + 5] for i in range(0, len(users), 5)]:
            if message.chat.id not in tagallgcid:
                break
            await asyncio.sleep(1.5)
            await m.reply_text(
                ", ".join(output) + "\n\n" + text, quote=bool(message.reply_to_message)
            )
        try:
            tagallgcid.remove(message.chat.id)
        except Exception:
            pass
    elif message.command[0] == "batal":
        if message.chat.id not in tagallgcid:
            return await eor(
                message, "Sedang tidak ada perintah: <code>tagall</code> yang digunakan"
            )
        try:
            tagallgcid.remove(message.chat.id)
        except Exception:
            pass
        await eor(message, "Ok tagall berhasil dibatalkan")
