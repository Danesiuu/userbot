import aiohttp
import filetype
from io import BytesIO
from PyroUbot import *
from httpx import AsyncClient, Timeout

fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)

async def upload_media(m):
    media = await m.reply_to_message.download()
    url = "https://itzpire.com/tools/upload"
    with open(media, "rb") as file:
        files = {"file": file}
        response = await fetch.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        link = data["fileInfo"]["url"]
        return link
    else:
        return f"{response.text}"

__MODULE__ = "ᴛᴏᴜʀʟ"
__HELP__ = """
<blockquote><b>╭〢BANTUAN UNTUK TOURL
││perintah : <code>{0}tourl</code> [ replay media ]
╰〢mengupload media ke link</blockquote></b>"""

@PY.UBOT("tourl|tg")
async def _(client, message):
    reply_message = message.reply_to_message
    if not reply_message:
        return await message.reply("Please reply to a media message to upload.")
    try:
        url = await upload_media(message)
    except Exception as e:
        return await message.reply(str(e))
    return await message.reply(f"**Successfully Uploaded: <a href='{url}'>link potonya</a>**", disable_web_page_preview=True)
        
