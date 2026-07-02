# movies/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movie/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("movie/<int:pk>/stream/", views.stream_video, name="stream_video"),
    path("like/<int:id>/", views.like, name="like"),
    path('list/', views.kino_list, name="kino_list"),
    # Bot uchun ichki API
    path("api/movies/add_file/", views.add_file, name="add_file"),
    # Authentication
    path("login/", views.custom_login, name="login"),
    path("signup/", views.custom_signup, name="signup"),
    path("logout/", views.custom_logout, name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            html_email_template_name='registration/password_reset_email.html'
        ),
        name="password_reset"
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    ),
]