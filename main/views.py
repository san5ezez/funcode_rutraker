import os
import random
from itertools import cycle

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import UserGameForm, UserRegistrationForm, GameRequestForm
from .models import UserGame
from main.management.commands.rutracker import RuTracker  # Если используешь RuTracker

# Папка с картинками
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), '1')


def format_size(size):
    """Форматирование размера в MB или GB."""
    size = int(size) / (1024 * 1024)
    if size >= 1024:
        return f"{size / 1024:.2f} GB"
    return f"{size:.2f} MB"


def index(request):
    query = request.GET.get("q", "").lower()
    sort_by = request.GET.get("sort", "")

    games = []

    if query:
        # Проверка: только для авторизованных
        if not request.user.is_authenticated:
            return render(request, "main/index.html", {
                "games": [],
                "query": query,
                "sort_by": sort_by,
                "message": "Для поиска игр нужно войти в аккаунт."
            })

        # Поиск через RuTracker (или свои игры)
        try:
            engine = RuTracker()
            engine.search(query)
            for torrent_id, torrent_data in engine.results.items():
                games.append({
                    "title": torrent_data["name"],
                    "rutracker_id": torrent_id,
                    "category": "RuTracker",
                    "seeds": int(torrent_data["seeds"]),
                    "size_readable": format_size(torrent_data["size"]),
                    "size": int(torrent_data["size"]),
                    "image": random.choice(os.listdir(IMAGE_FOLDER)),
                    "link": torrent_data["desc_link"],
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

    return render(request, "main/index.html", {
        "games": games,
        "query": query,
        "sort_by": sort_by,
    })


# ------------------------
# Регистрация пользователя
# ------------------------
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


# ------------------------
# Отправка запроса на добавление игры
# ------------------------
@login_required
def game_request(request):
    if request.method == 'POST':
        form = GameRequestForm(request.POST, request.FILES)
        if form.is_valid():
            game_request = form.save(commit=False)
            game_request.user = request.user
            game_request.save()
            return redirect('index')
    else:
        form = GameRequestForm()
    return render(request, 'main/game_request.html', {'form': form})


# ------------------------
# Добавление игры пользователем
# ------------------------
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


# ------------------------
# Кастомный LoginView
# ------------------------
class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    authentication_form = AuthenticationForm
