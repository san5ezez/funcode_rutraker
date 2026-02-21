# main/urls.py
from django.urls import path
from .views import index, register, game_request, add_user_game

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("game-request/", game_request, name="game_request"),
    path("add-user-game/", add_user_game, name="add_user_game"),
]
