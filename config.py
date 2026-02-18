import os
import internetarchive

BOT_TOKEN = os.getenv("BOT_TOKEN")
IA_ACCESS = os.getenv("IA_ACCESS")
IA_SECRET = os.getenv("IA_SECRET")

DOWNLOAD_FOLDER = "downloads"

internetarchive.configure(IA_ACCESS, IA_SECRET)
