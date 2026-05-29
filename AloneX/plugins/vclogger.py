import asyncio
import random
from logging import getLogger
from typing import Dict, Set

from pyrogram import filters
from pyrogram.types import Message

from AloneX import app

# ---------------- SAFE DB IMPORT ----------------
try:
    from AloneX import mongodb
except:
    from AloneX import db as mongodb

LOGGER = getLogger(__name__)

vc_active_users: Dict[int, Set[int]] = {}
active_vc_chats: Set[int] = set()
vc_logging_status: Dict[int, bool] = {}

# SAFE COLLECTION
try:
    vcloggerdb = mongodb.vclogger
except:
    vcloggerdb = None

prefixes = [".", "!", "/", "@", "?", "'"]

# ---------------- LOAD STATUS ----------------
async def load_vc_logger_status():
    if not vcloggerdb:
        return

    try:
        cursor = vcloggerdb.find({})
        async for doc in cursor:
            chat_id = doc.get("chat_id")
            status = doc.get("status", False)

            vc_logging_status[chat_id] = status

            if status:
                asyncio.create_task(check_and_monitor_vc(chat_id))

        LOGGER.info(f"VC Logger Loaded: {len(vc_logging_status)} chats")

    except Exception as e:
        LOGGER.error(f"Load Error: {e}")


# ---------------- SAVE STATUS ----------------
async def save_vc_logger_status(chat_id: int, status: bool):
    if not vcloggerdb:
        return

    try:
        await vcloggerdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"chat_id": chat_id, "status": status}},
            upsert=True
        )
    except Exception as e:
        LOGGER.error(f"Save Error: {e}")


# ---------------- GET STATUS ----------------
async def get_vc_logger_status(chat_id: int) -> bool:
    return vc_logging_status.get(chat_id, False)


# ---------------- COMMAND ----------------
@app.on_message(filters.command("vclogger", prefixes=prefixes) & filters.group)
async def vclogger_command(_, message: Message):

    chat_id = message.chat.id
    args = message.text.split()

    status = await get_vc_logger_status(chat_id)

    if len(args) == 1:
        return await message.reply(
            f"📌 VC Logger: {status}\n\nUse:\n/vclogger on\n/vclogger off"
        )

    arg = args[1].lower()

    if arg in ["on", "enable", "yes"]:

        vc_logging_status[chat_id] = True
        await save_vc_logger_status(chat_id, True)

        await message.reply("✅ VC Logger Enabled")

        asyncio.create_task(check_and_monitor_vc(chat_id))

    elif arg in ["off", "disable", "no"]:

        vc_logging_status[chat_id] = False
        await save_vc_logger_status(chat_id, False)

        active_vc_chats.discard(chat_id)
        vc_active_users.pop(chat_id, None)

        await message.reply("❌ VC Logger Disabled")

    else:
        await message.reply("❌ Invalid Usage")


# ---------------- CHECK ----------------
async def check_and_monitor_vc(chat_id):

    if not vc_logging_status.get(chat_id):
        return

    if chat_id in active_vc_chats:
        return

    active_vc_chats.add(chat_id)
    asyncio.create_task(monitor_vc_chat(chat_id))


# ---------------- MONITOR (SAFE LOOP) ----------------
async def monitor_vc_chat(chat_id):

    while vc_logging_status.get(chat_id):

        try:
            await asyncio.sleep(15)

        except Exception as e:
            LOGGER.error(f"Monitor Error: {e}")


# ---------------- USER JOIN ----------------
async def handle_user_join(chat_id, user_id):
    try:
        user = await app.get_users(user_id)

        name = user.first_name or "User"
        username = f"@{user.username}" if user.username else "No Username"

        mention = f'<a href="tg://user?id={user_id}"><b>{name}</b></a>'

        msg = random.choice([
            f"🎤 {mention} joined VC\n👤 {username}",
            f"🔥 {mention} entered voice chat\n👤 {username}",
            f"✨ {mention} is now in VC\n👤 {username}"
        ])

        await app.send_message(chat_id, msg)

    except Exception as e:
        LOGGER.error(f"Join Error: {e}")


# ---------------- USER LEAVE ----------------
async def handle_user_leave(chat_id, user_id):
    try:
        user = await app.get_users(user_id)

        name = user.first_name or "User"
        username = f"@{user.username}" if user.username else "No Username"

        mention = f'<a href="tg://user?id={user_id}"><b>{name}</b></a>'

        msg = random.choice([
            f"👋 {mention} left VC\n👤 {username}",
            f"💔 {mention} exited voice chat\n👤 {username}",
            f"🚪 {mention} went offline\n👤 {username}"
        ])

        await app.send_message(chat_id, msg)

    except Exception as e:
        LOGGER.error(f"Leave Error: {e}")


# ---------------- INIT ----------------
async def initialize_vc_logger():
    await load_vc_logger_status()
