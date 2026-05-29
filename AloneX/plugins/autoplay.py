from pyrogram import filters
from pyrogram.types import Message
from AloneX import app

# Store autoplay status
autoplay_status = {}


# ================== AUTOPLAY COMMAND ================== #

@app.on_message(filters.command("autoplay"))
async def toggle_autoplay(client, message: Message):
    chat_id = message.chat.id

    # Check argument
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
            "✅ Autoplay Enabled.\n"
            "Songs will now play automatically."
        )

    elif option == "disable":
        autoplay_status[chat_id] = False
        await message.reply_text(
            "❌ Autoplay Disabled."
        )

    else:
        await message.reply_text(
            "Invalid Option.\nUse:\n"
            "/autoplay enable\n"
            "/autoplay disable"
        )


# ================== AUTOPLAY FUNCTION ================== #

async def auto_play(chat_id):

    # Check enabled or not
    if not autoplay_status.get(chat_id):
        return

    try:
        # Example song query
        query = "Latest Hindi Songs"

        # Yaha tumhara play function call hoga
        # Example:
        # await play_song(chat_id, query)

        print(f"Autoplaying in {chat_id}")

    except Exception as e:
        print(e)
