from pyrogram import filters
import asyncio
from pyrogram import client
from Barath import barath
from Barath.helpers.help_func import get_arg
import Barath.barath_db.afk_db as Zect
from Barath.helpers.help_func import user_afk
from Barath import get_readable_time
from Barath.helpers.utils import get_message_type, Types
from config import HANDLER, OWNER_ID, GROUP_ID
from Barath.helpers.help_func import get_datetime 
import time


MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 20


@barath.on_message(filters.command("afk", HANDLER) & filters.me)
async def afk(barath, message):
    afk_time = int(time.time())
    arg = get_arg(message)
    if not arg:
        reason = None
    else:
        reason = arg
    await Zect.set_afk(True, afk_time, reason)
    await message.edit("**╔══════════════════════════╗\n\n Hᴇʏ ☯️  Mʏ Mᴀsᴛᴇʀ 🌟🌟 Is Sɪɴᴄᴇ Oғғʟɪɴᴇ Fᴏʀ A Wʜɪʟᴇ , Sᴏᴏɴ Hᴇ Wɪʟʟ Bᴀᴄᴋ Tᴏ Rᴇᴘʟʏ 👍\n\n 𝙳𝚘𝚗'𝚝 𝚂𝚙𝚊𝚖 🚫 𝙱𝚎 𝙿𝚊𝚝𝚒𝚎𝚗𝚝 😐\n\n ╚══════════════════════════╝**")


@barath.on_message(filters.mentioned & ~filters.bot & filters.create(user_afk), group=11)
async def afk_mentioned(_, message):
    global MENTIONED
    afk_time, reason = await Zect.afk_stuff()
    afk_since = get_readable_time(time.time() - afk_time)
    if "-" in str(message.chat.id):
        cid = str(message.chat.id)[4:]
    else:
        cid = str(message.chat.id)

    if cid in list(AFK_RESTIRECT) and int(AFK_RESTIRECT[cid]) >= int(time.time()):
        return
    AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME
    if reason:
       await message.reply(
        f"╔══════════════════════════╗\n\n Hᴇʏ ☯️  Mʏ Mᴀsᴛᴇʀ 🌟🌟 Is Sɪɴᴄᴇ Oғғʟɪɴᴇ Fᴏʀ A Wʜɪʟᴇ , Sᴏᴏɴ Hᴇ Wɪʟʟ Bᴀᴄᴋ Tᴏ Rᴇᴘʟʏ 👍\n\n **AFK 》(Since{afk_since})**\n **Reason 》__{reason}__**\n\n 𝙳𝚘𝚗'𝚝 𝚂𝚙𝚊𝚖 🚫 𝙱𝚎 𝙿𝚊𝚝𝚒𝚎𝚗𝚝 😐\n\n ╚══════════════════════════╝"
        )
    else:
        await message.reply(f"**╔══════════════════════════╗\n\n Hᴇʏ ☯️  Mʏ Mᴀsᴛᴇʀ 🌟🌟 Is Sɪɴᴄᴇ Oғғʟɪɴᴇ Fᴏʀ A Wʜɪʟᴇ , Sᴏᴏɴ Hᴇ Wɪʟʟ Bᴀᴄᴋ Tᴏ Rᴇᴘʟʏ 👍\n\n AFK 》(Since{afk_since}) 𝙳𝚘𝚗'𝚝 𝚂𝚙𝚊𝚖 🚫 𝙱𝚎 𝙿𝚊𝚝𝚒𝚎𝚗𝚝 😐\n\n ╚══════════════════════════╝**")

        _, message_type = get_message_type(message)
        if message_type == Types.TEXT:
            text = message.text or message.caption
        else:
            text = message_type.name

        MENTIONED.append(
            {
                "user": message.from_user.first_name,
                "user_id": message.from_user.id,
                "chat": message.chat.title,
                "chat_id": cid,
                "text": text,
                "message_id": message.message_id,
            }
        )


@barath.on_message(filters.create(user_afk) & filters.outgoing)
async def auto_unafk(_, message):
    await Zect.set_unafk()
    unafk_message = await barath.send_message(message.chat.id, "**WELCOME BACK BY @THE_AKITO Family**")
    global MENTIONED
    text = "**Total {} mentioned you**\n".format(len(MENTIONED))
    for x in MENTIONED:
        msg_text = x["text"]
        if len(msg_text) >= 11:
            msg_text = "{}...".format(x["text"])
        text += "- [{}](https://t.me/c/{}/{}) ({}): {}\n".format(
            x["user"],
            x["chat_id"],
            x["message_id"],
            x["chat"],
            msg_text,
        )
        await barath.send_message(GROUP_ID, text)
        MENTIONED = []
    await asyncio.sleep(2)
    await unafk_message.delete()
