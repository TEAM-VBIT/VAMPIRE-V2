from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", "39665202"))
        self.API_HASH = getenv("API_HASH", "97e021acb4dd34a06986576fc7214ec7")

        self.BOT_TOKEN = getenv("BOT_TOKEN", "8009946964:AAEuxRA9yNsTtvi3TrnP Dxw71ujDWxj1swA")
        self.MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Jani_Sanatani_Power:RamRP@jani.elxnxrd.mongodb.net/?appName=Jani")

        self.LOGGER_ID = int(getenv("LOGGER_ID", "-1003280956735"))
        self.OWNER_ID = int(getenv("OWNER_ID", "5576295421"))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 10800)) * 10800
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 20))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 20))

        self.SESSION1 = getenv("SESSION", "BQJdPjIAop9JvEbBYduPhxJ1ny5_edjVHtgCnTD8V_MzmK2aDG6rnn6qvZQ8WdBlzYk7mVgXgAiCGjYV8Wc7Was6E76OOMF7doyrj3BWil28nVj0fbl5mJhjuTH0reA7Wejq235QSAWW7inaIPTwrbD27G3ce-X3T5C7msZUsuQb45CQ4vdbFl7yujc5tcZaRq2bRVIKEzsjFdPKDIe8EG02Q_hMy9y7KsZyJKM771xThAsyefxTXrOvn7ENnjYvsjI6REbfCRNCEgbN2eaU6sDBiwl6YP8-VSvsSIL34OtDOK7DszhnlxkF5QW8G_JkZ5nNo1aSOzA32JUPHUfcdbQNIGrWZAAAAAH77avAAA")
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/LunaBots1")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Luna_Support_Team")

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
        self.START_IMG = getenv("START_IMG", "https://files.catbox.moe/3gtxpg.jpg")

    def check(self):
        missing = [
            var
            for var in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID", "SESSION1"]
            if not getattr(self, var)
        ]
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
