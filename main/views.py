
import os
import asyncio
from django.conf import settings
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
import json

from telethon import TelegramClient
from telethon.sessions import StringSession

from .models import Movie


# ─── Telethon client ──────────────────────────────────────────────────────────

def get_client() -> TelegramClient:
    return TelegramClient(
        StringSession(settings.TELEGRAM_SESSION),
        settings.TELEGRAM_API_ID,
        settings.TELEGRAM_API_HASH,
    )


def run_async(coro):
    """Django sync muhitida async kodni ishlatish."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ─── Stream ───────────────────────────────────────────────────────────────────

async def _iter_file_chunks(message_id: int, start: int, end: int | None):
    """
    Telegram kanaldan faylni chunk larga bo'lib beradi.
    message_id — kanalga yuklangan xabar raqami.
    """
    async with get_client() as client:
        channel = settings.TELEGRAM_CHANNEL  # masalan: -1001234567890
        message = await client.get_messages(channel, ids=message_id)

        if not message or not message.media:
            return

        # offset va limit hisoblash
        chunk_size = 1024 * 1024  # 1 MB

        async for chunk in client.iter_download(
            message.media,
            offset=start,
            limit=(end - start + 1) if end else None,
            chunk_size=chunk_size,
            dc_id=message.media.document.dc_id if hasattr(message.media, 'document') else None,
        ):
            yield chunk


def stream_video(request, pk):
    """
    Range header ni qo'llab-quvvatlaydigan video stream.
    Seek qilish ishlaydi.
    """
    movie = get_object_or_404(Movie, pk=pk, is_active=True)

    if not movie.telegram_message_id:
        return JsonResponse({"error": "Message ID yo'q"}, status=404)

    # Fayl hajmini olish (keshdan)
    cache_key = f"movie_size_{pk}"
    file_size = cache.get(cache_key)

    if not file_size:
        async def get_size():
            async with get_client() as client:
                msg = await client.get_messages(
                    settings.TELEGRAM_CHANNEL,
                    ids=movie.telegram_message_id
                )
                if msg and msg.media and hasattr(msg.media, 'document'):
                    return msg.media.document.size
                return None

        file_size = run_async(get_size())
        if file_size:
            cache.set(cache_key, file_size, timeout=60 * 60 * 24)

    if not file_size:
        return JsonResponse({"error": "Fayl topilmadi"}, status=404)

    # Range header ni parse qilish
    range_header = request.META.get("HTTP_RANGE", "")
    start = 0
    end = file_size - 1
    status = 200

    if range_header:
        # "bytes=0-999999" → start=0, end=999999
        range_match = range_header.replace("bytes=", "").split("-")
        start = int(range_match[0]) if range_match[0] else 0
        end = int(range_match[1]) if range_match[1] else file_size - 1
        status = 206  # Partial Content

    content_length = end - start + 1

    # Sync generator — Django StreamingHttpResponse uchun
    def sync_generator():
        async def collect():
            chunks = []
            async for chunk in _iter_file_chunks(
                movie.telegram_message_id, start, end
            ):
                chunks.append(chunk)
            return chunks

        chunks = run_async(collect())
        for chunk in chunks:
            yield chunk

    response = StreamingHttpResponse(
        sync_generator(),
        status=status,
        content_type="video/mp4",
    )
    response["Content-Length"] = content_length
    response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
    response["Accept-Ranges"] = "bytes"

    return response


# ─── Sahifalar ────────────────────────────────────────────────────────────────

def home(request):
    movies = Movie.objects.filter(is_active=True)

    q = request.GET.get("q", "")
    if q:
        movies = movies.filter(title__icontains=q)

    genre = request.GET.get("genre", "")
    if genre:
        movies = movies.filter(genre__icontains=genre)

    genres = (
        Movie.objects.filter(is_active=True)
        .values_list("genre", flat=True)
        .distinct()
    )

    return render(request, "index.html", {
        "movies": movies,
        "genres": genres,
        "q": q,
        "genre": genre,
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk, is_active=True)
    Movie.objects.filter(pk=pk).update(views=movie.views + 1)
    return render(request, "detail.html", {"movie": movie})


# ─── Bot API (ichki) ──────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def add_file(request):
    api_key = request.headers.get("X-API-KEY", "")
    if api_key != settings.INTERNAL_API_KEY:
        return JsonResponse({"error": "Ruxsat yo'q"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON xato"}, status=400)

    file_id = data.get("file_id")
    message_id = data.get("message_id")
    caption = data.get("caption", "")

    if not file_id or not message_id:
        return JsonResponse({"error": "file_id va message_id kerak"}, status=400)

    lines = caption.strip().split("\n")
    title = lines[0] if lines and lines[0] else f"Kino #{message_id}"
    description = "\n".join(lines[1:]) if len(lines) > 1 else ""

    movie, created = Movie.objects.get_or_create(
        telegram_file_id=file_id,
        defaults={
            "title": title,
            "description": description,
            "telegram_message_id": message_id,
        },
    )

    return JsonResponse(
        {"id": movie.id, "title": movie.title, "created": created},
        status=201 if created else 200,
    )