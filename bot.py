# import logging
# import requests
# from telegram import Update
# from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
#
# # === SOZLAMALAR ===
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """
#     Kanalga yangi video kelganda avtomatik ishga tushadi.
#     Video file_id ni Django API ga yuboradi.
#     """
#     message = update.channel_post or update.message
#     if not message:
#         return
#
#     video = message.video or message.document
#     if not video:
#         return
#
#     file_id = video.file_id
#     caption = message.caption or ""
#
#     logger.info(f"Yangi video: file_id={file_id}, caption={caption}")
#
#     # Django API ga yuborish
#     try:
#         response = requests.post(
#             DJANGO_API_URL,
#             json={
#                 "file_id": file_id,
#                 "caption": caption,
#                 "message_id": message.message_id,
#             },
#             headers={"X-API-KEY": DJANGO_API_KEY},
#             timeout=10,
#         )
#         if response.status_code == 201:
#             logger.info("Muvaffaqiyatli saqlandi!")
#         else:
#             logger.error(f"Xato: {response.status_code} — {response.text}")
#     except Exception as e:
#         logger.error(f"API xatosi: {e}")
#
#
# def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()
#
#     # Kanal postlarini tinglash
#     app.add_handler(
#         MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video)
#     )
#
#     logger.info("Bot ishga tushdi...")
#     app.run_polling()
#
#
# if __name__ == "__main__":
#     main()
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors import FloodWaitError
from pathlib import Path
import random

# =========================
# TELEGRAM API MA'LUMOTLARI
# =========================
API_ID = 2131
API_HASH = ""
SESSION_NAME = "my_account"

UPDATE_INTERVAL = 10      # har 10 sekundda rasm yangilanadi
IMAGE_FOLDER = "image"    # rasmlar papkasi
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Avtomatik javob uchun
AUTO_REPLY_TEXT = (
    "Salom! 👋 Xabaringiz uchun rahmat.\n"
    "Hozir band bo'lsam ham, tez orada siz bilan bog'lanaman! 🙏"
)

# Bir xil odamga qayta-qayta javob bermaslik uchun
replied_users = set()


def get_images() -> list[Path]:
    """image/ papkasidagi barcha rasmlarni qaytaradi"""
    folder = Path(IMAGE_FOLDER)
    if not folder.exists():
        folder.mkdir()
        print(f"[INFO] '{IMAGE_FOLDER}' papkasi yaratildi. Rasmlarni shu joyga qo'ying.")
    images = [f for f in folder.iterdir() if f.suffix.lower() in PHOTO_EXTENSIONS]
    return images


async def update_photo(client: TelegramClient):
    """Papkadan tasodifiy rasm tanlab profilga qo'yadi"""
    images = get_images()
    if not images:
        print("[PHOTO] Rasmlar topilmadi! 'image/' papkasiga rasm qo'ying.")
        return

    chosen = random.choice(images)
    file = await client.upload_file(str(chosen))
    await client(UploadProfilePhotoRequest(file=file))
    print(f"[PHOTO] '{chosen.name}' → {datetime.now().strftime('%H:%M:%S')}")


async def update_bio(client: TelegramClient):
    """Bioga joriy vaqtni yozadi"""
    current_time = datetime.now().strftime("%H:%M")
    bio_text = f"🕒 {current_time} | Tashkent"
    await client(UpdateProfileRequest(about=bio_text))
    print(f"[BIO] Yangilandi: {bio_text}")


async def profile_loop(client: TelegramClient):
    """Har 10 sekundda rasm va bio yangilaydi"""
    while True:
        try:
            await update_photo(client)
            await update_bio(client)
        except FloodWaitError as e:
            wait = int(e.seconds) + 5
            print(f"[FloodWait] {wait} sekund kutaman...")
            await asyncio.sleep(wait)
            continue
        except Exception as e:
            print(f"[XATOLIK] {e}")

        await asyncio.sleep(UPDATE_INTERVAL)


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    print("✅ Telegram akkauntga ulandi.\n")

    # ================================
    # AVTOMATIK JAVOB (lichka xabarga)
    # ================================
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def auto_reply(event):
        sender_id = event.sender_id
        if sender_id in replied_users:
            return  # allaqachon javob berilgan

        replied_users.add(sender_id)
        await asyncio.sleep(1)  # biroz kutib javob beradi (tabiiyroq)
        await event.reply(AUTO_REPLY_TEXT)
        sender = await event.get_sender()
        name = getattr(sender, "first_name", "Noma'lum")
        print(f"[AUTO-REPLY] '{name}' ga javob berildi.")

    print("📸 Rasm yangilash va avtomatik javob ishga tushdi...\n")

    # Rasm loop va client birga ishlaydi
    await profile_loop(client)


if __name__ == "__main__":
    asyncio.run(main())