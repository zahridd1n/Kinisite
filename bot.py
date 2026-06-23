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
