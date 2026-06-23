# movies/models.py

from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    year = models.IntegerField(null=True, blank=True, verbose_name="Yili")
    genre = models.CharField(max_length=100, blank=True, verbose_name="Janri")
    poster = models.ImageField(upload_to="posters/", null=True, blank=True)

    # Telegram ma'lumotlari
    telegram_file_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Telegram file_id"
    )
    telegram_message_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Kino"
        verbose_name_plural = "Kinolar"

    def __str__(self):
        return self.title