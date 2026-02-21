from django.core.management.base import BaseCommand
from py_rutracker import RuTrackerClient
from py_rutracker.exceptions import RuTrackerAuthError
from main.models import Game


class Command(BaseCommand):
    help = "Импорт игр с RuTracker"

    def add_arguments(self, parser):
        parser.add_argument("query", type=str)

    def handle(self, *args, **options):
        query = options["query"]

        try:
            with RuTrackerClient("ЛОГИН", "ПАРОЛЬ") as client:
                results = client.search_with_form(
                    query,
                    sort_option=10,
                    sort_direction=2
                )

                for r in results:
                    Game.objects.update_or_create(
                        rutracker_id=str(r.topic_id),
                        defaults={
                            "title": r.title,
                            "size_readable": f"{r.size} {r.unit}",
                            "seeds": r.seedmed,
                            "category": r.category,
                        }
                    )

                self.stdout.write(self.style.SUCCESS(
                    f"Импортировано: {len(results)}"
                ))

        except RuTrackerAuthError:
            self.stderr.write(
                "❌ Капча. Зайди на RuTracker в браузере и повтори позже."
            )
