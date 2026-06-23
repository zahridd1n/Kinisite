from pyrogram import Client
from django.conf import settings

app = Client(
    "kino_stream",
    api_id=settings.TG_API_ID,
    api_hash=settings.TG_API_HASH,
    bot_token=settings.TG_BOT_TOKEN,
    in_memory=True
)