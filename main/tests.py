from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import UserGame


class UserGameFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass12345")

    def test_add_user_game_requires_authentication(self):
        response = self.client.get(reverse("add_user_game"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_user_can_add_game(self):
        self.client.login(username="tester", password="pass12345")

        response = self.client.post(
            reverse("add_user_game"),
            {
                "title": "Half Life",
                "description": "Classic",
                "size": 1024 * 1024,
                "seeds": 77,
            },
        )

        self.assertRedirects(response, reverse("index"))
        game = UserGame.objects.get(title="Half Life")
        self.assertEqual(game.user, self.user)

    def test_index_shows_user_game(self):
        UserGame.objects.create(
            user=self.user,
            title="Portal",
            description="Puzzle",
            size=2 * 1024 * 1024,
            seeds=15,
        )

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portal")
