import os
import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import GameRequestForm, UserGameForm, UserRegistrationForm
from .models import UserGame
from main.management.commands.rutracker import RuTracker

# Папка с картинками
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), '1')


def format_size(size):
    """Форматирование размера в MB или GB."""
    size = int(size) / (1024 * 1024)
    if size >= 1024:
        return f"{size / 1024:.2f} GB"
    return f"{size:.2f} MB"


def index(request):
    query = request.GET.get("q", "").strip().lower()
    sort_by = request.GET.get("sort", "")

    games = []

    # Игры, добавленные пользователями (показываем всегда).
    user_games_qs = UserGame.objects.select_related("user")
    if query:
        user_games_qs = user_games_qs.filter(title__icontains=query)

    for user_game in user_games_qs:
        games.append({
            "title": user_game.title,
            "category": f"Пользователь: {user_game.user.username}",
            "seeds": user_game.seeds,
            "size_readable": user_game.size_readable(),
            "size": user_game.size,
            "image": user_game.image.url if user_game.image else "",
            "rutracker_id": None,
            "link": user_game.download_url,
            "trailer_url": user_game.trailer_url,
            "screenshot": user_game.screenshot.url if user_game.screenshot else "",
        })

    if query and request.user.is_authenticated:
        # Поиск через RuTracker для авторизованных пользователей.
        try:
            engine = RuTracker()
            engine.search(query)
            image_choices = os.listdir(IMAGE_FOLDER)
            for torrent_id, torrent_data in engine.results.items():
                games.append({
                    "title": torrent_data["name"],
                    "rutracker_id": torrent_id,
                    "category": "RuTracker",
                    "seeds": int(torrent_data["seeds"]),
                    "size_readable": format_size(torrent_data["size"]),
                    "size": int(torrent_data["size"]),
                    "image": f"/static/{random.choice(image_choices)}" if image_choices else "",
                    "link": torrent_data["desc_link"],
                    "trailer_url": "",
                    "screenshot": "",
                })
        except Exception as e:
            print(f"Ошибка при поиске на RuTracker: {e}")

    # Сортировка
    if sort_by == "size_asc":
        games.sort(key=lambda x: x["size"])
    elif sort_by == "size_desc":
        games.sort(key=lambda x: x["size"], reverse=True)
    elif sort_by == "name_asc":
        games.sort(key=lambda x: x["title"].lower())
    elif sort_by == "name_desc":
        games.sort(key=lambda x: x["title"].lower(), reverse=True)
    elif sort_by == "seeds_desc":
        games.sort(key=lambda x: x["seeds"], reverse=True)
    elif sort_by == "seeds_asc":
        games.sort(key=lambda x: x["seeds"])

    message = ""
    if query and not request.user.is_authenticated:
        message = "Результаты RuTracker доступны после входа в аккаунт."

    return render(request, "main/index.html", {
        "games": games,
        "query": query,
        "sort_by": sort_by,
        "message": message,
    })


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def game_request(request):
    if request.method == 'POST':
        form = GameRequestForm(request.POST, request.FILES)
        if form.is_valid():
            game_request_obj = form.save(commit=False)
            game_request_obj.user = request.user
            game_request_obj.save()
            return redirect('index')
    else:
        form = GameRequestForm()
    return render(request, 'main/game_request.html', {'form': form})


@login_required
def add_user_game(request):
    if request.method == 'POST':
        form = UserGameForm(request.POST, request.FILES)
        if form.is_valid():
            user_game = form.save(commit=False)
            user_game.user = request.user
            user_game.save()
            return redirect('index')
    else:
        form = UserGameForm()
    return render(request, 'main/add_user_game.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return self.get_redirect_url() or '/'
