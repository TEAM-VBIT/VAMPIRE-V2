from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", "24832"))
        self.API_HASH = getenv("API_HASH", "caff31b386e4a0")

        self.BOT_TOKEN = getenv("BOT_TOKEN", "8629527009:AAGbrehqLedDjGnG3dw42WK7NN1tTaIAVRU")
        self.MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Jani_Sanatani_Power:RamRP@jani.elxnxrd.mongodb.net/?appName=Jani")

        self.LOGGER_ID = int(getenv("LOGGER_ID", "-1003280956735"))
        self.OWNER_ID = int(getenv("OWNER_ID", "5099526956"))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 10800)) * 10800
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 20))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 20))

        self.SESSION1 = getenv("SESSION", "BQIcsSwACE2PlJV0YTF2ybYtI8oftSMXh3wAAAAIBjtNYAA")
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/LunaBots1")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/+1L0u7kV8LLI0NTI1")

        self.AUTO_END: bool = getenv("AUTO_END", False)
        self.AUTO_LEAVE: bool = getenv("AUTO_LEAVE", False)
        self.VIDEO_PLAY: bool = getenv("VIDEO_PLAY", True)
        self.COOKIES_URL = [
            url for url in getenv("COOKIES_URL", "").split(" ")
            if url and "batbin.me" in url
        ]
        self.YOUTUBE_API_KEY = getenv("YOUTUBE_API_KEY", "INFLEX25174928D")
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://te.legra.ph/file/3e40a408286d4eda24191.jpg")
        self.PING_IMG = getenv("PING_IMG", "https://files.catbox.moe/haagg2.png")
        self.START_IMG = getenv("START_IMG", "https://files.catbox.moe/zvziwk.jpg")

    def check(self):
        missing = [
            var
            for var in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID", "SESSION1"]
            if not getattr(self, var)
        ]
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
