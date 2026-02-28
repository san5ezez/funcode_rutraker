from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import GameRequest, UserGame


class UserGameFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass12345")

    def test_game_request_requires_authentication(self):
        response = self.client.get(reverse("game_request"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_user_can_create_game_request(self):
        self.client.login(username="tester", password="pass12345")

        image_file = SimpleUploadedFile(
            "cover.jpg",
            b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;",
            content_type="image/jpeg",
        )

        response = self.client.post(
            reverse("game_request"),
            {
                "name": "Half Life 3",
                "description": "Хотим новую часть",
                "requirements": "8 GB RAM",
                "reviews": "Будет хит",
                "trailer_url": "https://example.com/trailer",
                "image": image_file,
            },
        )

        self.assertRedirects(response, reverse("game_requests_status"))
        created = GameRequest.objects.get(name="Half Life 3")
        self.assertEqual(created.user, self.user)
        self.assertEqual(created.status, "pending")


    def test_game_request_accepts_iframe_in_trailer_field(self):
        self.client.login(username="tester", password="pass12345")

        image_file = SimpleUploadedFile(
            "cover.jpg",
            b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;",
            content_type="image/jpeg",
        )

        iframe = '<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/nSE38xjMLqE?si=32sbN0fUbEoGNkE_&amp;controls=0" title="YouTube video player" frameborder="0" allowfullscreen></iframe>'

        response = self.client.post(
            reverse("game_request"),
            {
                "name": "Half Life 4",
                "description": "iframe test",
                "requirements": "8 GB RAM",
                "reviews": "ok",
                "trailer_url": iframe,
                "image": image_file,
            },
        )

        self.assertRedirects(response, reverse("game_requests_status"))
        created = GameRequest.objects.get(name="Half Life 4")
        self.assertEqual(
            created.trailer_url,
            "https://www.youtube-nocookie.com/embed/nSE38xjMLqE?si=32sbN0fUbEoGNkE_&controls=0",
        )

    def test_index_shows_approved_game_request(self):
        GameRequest.objects.create(
            user=self.user,
            name="Approved Game",
            description="desc",
            requirements="req",
            reviews="rev",
            trailer_url="https://example.com/trailer",
            status="approved",
            image="game_requests/approved.jpg",
        )

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Game")
        self.assertContains(response, "Одобрено")

    def test_approved_game_request_detail_is_available(self):
        approved = GameRequest.objects.create(
            user=self.user,
            name="Approved Detail",
            description="desc",
            requirements="req",
            reviews="rev",
            trailer_url="https://example.com/trailer",
            status="approved",
            image="game_requests/approved_detail.jpg",
        )

        response = self.client.get(reverse("approved_game_request_detail", args=[approved.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Detail")

    def test_non_approved_game_request_detail_not_available(self):
        pending = GameRequest.objects.create(
            user=self.user,
            name="Pending Detail",
            description="desc",
            requirements="req",
            reviews="rev",
            trailer_url="https://example.com/trailer",
            status="pending",
            image="game_requests/pending_detail.jpg",
        )

        response = self.client.get(reverse("approved_game_request_detail", args=[pending.id]))

        self.assertEqual(response.status_code, 404)

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


class GameRequestStatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="statususer", password="pass12345")

    def test_status_page_filter(self):
        self.client.login(username="statususer", password="pass12345")
        GameRequest.objects.create(
            user=self.user,
            name="Game A",
            description="a",
            requirements="r",
            reviews="v",
            trailer_url="https://example.com/a",
            status="approved",
            image="game_requests/a.jpg",
        )
        GameRequest.objects.create(
            user=self.user,
            name="Game B",
            description="b",
            requirements="r",
            reviews="v",
            trailer_url="https://example.com/b",
            status="pending",
            image="game_requests/b.jpg",
        )

        response = self.client.get(reverse("game_requests_status"), {"status": "approved"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Game A")
        self.assertNotContains(response, "Game B")


class AuthFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="authuser", password="pass12345")

    def test_login_redirects_to_index(self):
        response = self.client.post(reverse("login"), {"username": "authuser", "password": "pass12345"})
        self.assertRedirects(response, reverse("index"))
