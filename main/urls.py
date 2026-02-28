# main/urls.py
from django.urls import path
from .views import index, register, game_request, add_user_game, user_game_detail

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("game-request/", game_request, name="game_request"),
    path("add-user-game/", add_user_game, name="add_user_game"),
    path("user-games/<int:game_id>/", user_game_detail, name="user_game_detail"),
]
