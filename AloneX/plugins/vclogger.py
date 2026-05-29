import asyncio
import random

from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.raw import functions

from AloneX import app, mongodb
from AloneX.utils.database import get_assistant

LOGGER = getLogger(__name__)

vc_active_users: Dict[int, Set[int]] = {}
active_vc_chats: Set[int] = set()
vc_logging_status: Dict[int, bool] = {}

vcloggerdb = mongodb.vclogger

prefixes = [".", "!", "/", "@", "?", "'"]


async def load_vc_logger_status():

    try:

        cursor = vcloggerdb.find({})

        enabled_chats = []

        async for doc in cursor:

            chat_id = doc["chat_id"]
            status = doc["status"]

            vc_logging_status[chat_id] = status

            if status:
                enabled_chats.append(chat_id)

        for chat_id in enabled_chats:
            asyncio.create_task(
                check_and_monitor_vc(chat_id)
            )

        LOGGER.info(
            f"Loaded VC logger status for {len(vc_logging_status)} chats"
        )

    except Exception as e:

        LOGGER.error(
            f"Error loading VC logger status: {e}"
        )


async def save_vc_logger_status(
    chat_id: int,
    status: bool
):

    try:

        await vcloggerdb.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "chat_id": chat_id,
                    "status": status
                }
            },
            upsert=True
        )

    except Exception as e:

        LOGGER.error(
            f"Error saving VC logger status: {e}"
        )


async def get_vc_logger_status(
    chat_id: int
) -> bool:

    if chat_id in vc_logging_status:
        return vc_logging_status[chat_id]

    try:

        doc = await vcloggerdb.find_one(
            {"chat_id": chat_id}
        )

        if doc:

            status = doc["status"]

            vc_logging_status[chat_id] = status

            return status

    except Exception as e:

        LOGGER.error(
            f"Error getting VC logger status: {e}"
        )

    return False


def generate_vclogger_filters():

    return (
        filters.command(
            "vclogger",
            prefixes=prefixes
        )
        & filters.group
    )


@app.on_message(generate_vclogger_filters())
async def vclogger_command(
    _,
    message: Message
):

    chat_id = message.chat.id

    args = message.text.split()

    status = await get_vc_logger_status(
        chat_id
    )

    current_state_ui = to_small_caps(
        str(status)
    )

    if len(args) == 1:

        return await message.reply(
            f"""
📌 <b>VC Logger Status :</b> <b>{current_state_ui}</b>

<b>Usage :</b>

<code>/vclogger on</code>
<code>/vclogger off</code>
"""
        )

    arg = args[1].lower()

    if arg in [
        "on",
        "enable",
        "yes"
    ]:

        vc_logging_status[chat_id] = True

        await save_vc_logger_status(
            chat_id,
            True
        )

        await message.reply(
            "✅ VC Logger Enabled"
        )

        asyncio.create_task(
            check_and_monitor_vc(chat_id)
        )

    elif arg in [
        "off",
        "disable",
        "no"
    ]:

        vc_logging_status[chat_id] = False

        await save_vc_logger_status(
            chat_id,
            False
        )

        active_vc_chats.discard(chat_id)

        vc_active_users.pop(
            chat_id,
            None
        )

        await message.reply(
            "❌ VC Logger Disabled"
        )

    else:

        await message.reply(
            "❌ Invalid Usage"
        )


async def get_group_call_participants(
    userbot,
    peer
):

    try:

        full_chat = await userbot.invoke(
            functions.channels.GetFullChannel(
                channel=peer
            )
        )

        if (
            not hasattr(
                full_chat.full_chat,
                "call"
            )
            or not full_chat.full_chat.call
        ):
            return []

        call = full_chat.full_chat.call

        participants = await userbot.invoke(
            functions.phone.GetGroupParticipants(
                call=call,
                ids=[],
                sources=[],
                offset="",
                limit=100
            )
        )

        return participants.participants

    except Exception as e:

        LOGGER.error(
            f"Error fetching participants: {e}"
        )

        return []


async def monitor_vc_chat(chat_id):

    userbot = await get_assistant(chat_id)

    if not userbot:
        return

    while (
        chat_id in active_vc_chats
        and await get_vc_logger_status(chat_id)
    ):

        try:

            peer = await userbot.resolve_peer(
                chat_id
            )

            participants_list = (
                await get_group_call_participants(
                    userbot,
                    peer
                )
            )

            new_users = set()

            for p in participants_list:

                if (
                    hasattr(p, "peer")
                    and hasattr(
                        p.peer,
                        "user_id"
                    )
                ):

                    new_users.add(
                        p.peer.user_id
                    )

            current_users = vc_active_users.get(
                chat_id,
                set()
            )

            joined = new_users - current_users

            left = current_users - new_users

            for user_id in joined:

                await handle_user_join(
                    chat_id,
                    user_id,
                    userbot
                )

            for user_id in left:

                await handle_user_leave(
                    chat_id,
                    user_id,
                    userbot
                )

            vc_active_users[chat_id] = new_users

        except Exception as e:

            LOGGER.error(
                f"Error monitoring VC: {e}"
            )

        await asyncio.sleep(15)


async def check_and_monitor_vc(chat_id):

    if not await get_vc_logger_status(chat_id):
        return

    userbot = await get_assistant(chat_id)

    if not userbot:
        return

    if chat_id not in active_vc_chats:

        active_vc_chats.add(chat_id)

        asyncio.create_task(
            monitor_vc_chat(chat_id)
        )


async def handle_user_join(
    chat_id,
    user_id,
    userbot
):

    try:

        user = await userbot.get_users(
            user_id
        )

        name = user.first_name or "Someone"

        mention = (
            f'<a href="tg://user?id={user_id}">'
            f'<b>{to_small_caps(name)}</b></a>'
        )

        messages = [

            f"🎤 {mention} <b>ᴊᴏɪɴᴇᴅ ᴠᴄ</b>",

            f"✨ {mention} <b>ʙᴀʙʏ ᴄᴏᴍᴇ ᴛᴏ ᴠᴄ</b>",

            f"🔥 {mention} <b>ᴇɴᴛᴇʀᴇᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ</b>",
        ]

        sent = await app.send_message(
            chat_id,
            random.choice(messages)
        )

        asyncio.create_task(
            delete_after_delay(
                sent,
                10
            )
        )

    except Exception as e:

        LOGGER.error(
            f"Join Error: {e}"
        )


async def handle_user_leave(
    chat_id,
    user_id,
    userbot
):

    try:

        user = await userbot.get_users(
            user_id
        )

        name = user.first_name or "Someone"

        mention = (
            f'<a href="tg://user?id={user_id}">'
            f'<b>{to_small_caps(name)}</b></a>'
        )

        messages = [

            f"👋 {mention} <b>ʟᴇꜰᴛ ᴠᴄ</b>",

            f"💔 {mention} <b>ᴇxɪᴛᴇᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ</b>",

            f"🚪 {mention} <b>ᴡᴇɴᴛ ᴏꜰꜰʟɪɴᴇ</b>",
        ]

        sent = await app.send_message(
            chat_id,
            random.choice(messages)
        )

        asyncio.create_task(
            delete_after_delay(
                sent,
                10
            )
        )

    except Exception as e:

        LOGGER.error(
            f"Leave Error: {e}"
        )


async def delete_after_delay(
    message,
    delay
):

    try:

        await asyncio.sleep(delay)

        await message.delete()

    except:
        pass


def to_small_caps(text):

    mapping = {

        "a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ",
        "f":"ꜰ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ",
        "k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ",
        "p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ",
        "u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ",
        "z":"ᴢ"
    }

    return "".join(
        mapping.get(c.lower(), c)
        for c in text
    )


async def initialize_vc_logger():

    await load_vc_logger_status()
