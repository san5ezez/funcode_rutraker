from django.contrib import admin

from .models import Game, GameRequest, UserGame


@admin.register(UserGame)
class UserGameAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "size", "seeds", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("title", "description", "user__username")
    readonly_fields = ("created_at",)


@admin.register(GameRequest)
class GameRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "status", "created_at")
    list_filter = ("status", "created_at", "user")
    search_fields = ("name", "description", "requirements", "reviews", "user__username")
    readonly_fields = ("created_at",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "rutracker_id", "seeds", "category", "added_at")
    list_filter = ("category", "added_at")
    search_fields = ("title", "rutracker_id")
    readonly_fields = ("added_at",)
