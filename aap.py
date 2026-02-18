import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from utils import parse_caption, generate_identifier, upload_to_archive, cleanup_file
from config import BOT_TOKEN, DOWNLOAD_FOLDER

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.caption:
        await update.message.reply_text(
            "❌ Please provide caption:\n\nTitle: Your Title\nCategory: opensource_movies\nDescription: text"
        )
        return

    data = parse_caption(update.message.caption)
    title = data.get("title")
    category = data.get("category", "opensource_movies")
    description = data.get("description", "")

    if not title:
        await update.message.reply_text("❌ Title is required in caption.")
        return

    status = await update.message.reply_text("⏳ Downloading video...")

    video = update.message.video
    file = await context.bot.get_file(video.file_id)
    file_path = f"{DOWNLOAD_FOLDER}/{video.file_id}.mp4"
    await file.download_to_drive(file_path)

    identifier = generate_identifier(title)

    await status.edit_text("🚀 Uploading to Internet Archive...")

    try:
        await upload_to_archive(identifier, file_path, title, category, description)
        link = f"https://archive.org/details/{identifier}"
        await status.edit_text(f"✅ Upload Complete!\n🔗 {link}")

    except Exception as e:
        await status.edit_text(f"❌ Upload Failed\n{str(e)}")

    finally:
        cleanup_file(file_path)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    print("✅ Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
