# main/urls.py
from django.urls import path
from .views import index, register, game_request, user_game_detail, game_requests_status

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("game-request/", game_request, name="game_request"),
    path("game-requests-status/", game_requests_status, name="game_requests_status"),
    path("user-games/<int:game_id>/", user_game_detail, name="user_game_detail"),
]
