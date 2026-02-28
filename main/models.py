from django.db import models
from django.contrib.auth.models import User

class UserGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    size = models.PositiveIntegerField(default=0, help_text="Размер в байтах")
    seeds = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='user_games/', blank=True, null=True)
    screenshot = models.ImageField(upload_to='user_games/screenshots/', blank=True, null=True)
    trailer_url = models.URLField(blank=True)
    download_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def size_readable(self):
        if self.size >= 1024*1024*1024:
            return f"{self.size / (1024*1024*1024):.2f} GB"
        return f"{self.size / (1024*1024):.2f} MB"

    def __str__(self):
        return self.title

class GameRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "На рассмотрении"),
        (STATUS_APPROVED, "Одобрено"),
        (STATUS_REJECTED, "Не одобрено"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    reviews = models.TextField()
    trailer_url = models.URLField()
    image = models.ImageField(upload_to='game_requests/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=500)
    rutracker_id = models.CharField(max_length=50, unique=True)
    size_readable = models.CharField(max_length=50, blank=True)
    seeds = models.IntegerField(default=0)
    category = models.CharField(max_length=255, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


