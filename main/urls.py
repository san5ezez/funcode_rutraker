# main/urls.py
from django.urls import path
from .views import index, register, game_request

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("game-request/", game_request, name="game_request"),
]
