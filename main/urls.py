# movies/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movie/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("movie/<int:pk>/stream/", views.stream_video, name="stream_video"),

    # Bot uchun ichki API
    path("api/movies/add_file/", views.add_file, name="add_file"),
]