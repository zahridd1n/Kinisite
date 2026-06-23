from django.apps import AppConfig
import asyncio


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self):
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(self.start_telegram())
        except:
            pass

    async def start_telegram(self):
        from .telegram_client import app

        if not app.is_connected:
            await app.start()