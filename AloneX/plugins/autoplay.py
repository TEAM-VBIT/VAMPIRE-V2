from pyrogram import filters
from pyrogram.types import Message

from AloneX import app, yt, anon, queue

# ================= STORE ================= #

autoplay_status = {}

# ================= COMMAND ================= #

@app.on_message(filters.command("autoplay"))
async def toggle_autoplay(client, message: Message):

    chat_id = message.chat.id

    if len(message.command) < 2:

        return await message.reply_text(
            "Usage:\n"
            "/autoplay enable\n"
            "/autoplay disable"
        )

    option = message.command[1].lower()

    if option == "enable":

        autoplay_status[chat_id] = True

        await message.reply_text(
            "✅ Autoplay Enabled"
        )

    elif option == "disable":

        autoplay_status[chat_id] = False

        await message.reply_text(
            "❌ Autoplay Disabled"
        )

    else:

        await message.reply_text(
            "Invalid Usage.\n"
            "/autoplay enable\n"
            "/autoplay disable"
        )

# ================= AUTOPLAY ================= #

async def auto_play(chat_id):

    if not autoplay_status.get(chat_id):
        return

    try:

        query = "Latest Hindi Songs"

        file = await yt.search(
            query,
            0,
            video=False,
        )

        if not file:
            return

        # Queue add
        queue.add(chat_id, file)

        # Download
        if not file.file_path:

            file.file_path = await yt.download(
                file.id,
                video=False,
            )

        # Play directly
        await anon.play_media(
            chat_id=chat_id,
            message=await app.send_message(
                chat_id,
                "🎵 Autoplaying Next Song..."
            ),
            media=file,
        )

    except Exception as e:
        print(f"AUTOPLAY ERROR : {e}")
