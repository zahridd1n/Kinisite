"""
Bu skriptni BIR MARTA ishga tushiring — session string olish uchun.
Keyin natijani .env ga saqlang: TELEGRAM_SESSION=...

Ishlatish:
    pip install telethon
    python get_session.py
"""

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = int(input("API_ID: "))
API_HASH = input("API_HASH: ")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("\n✅ Session string (buni .env ga saqlang):")
    print(client.session.save())