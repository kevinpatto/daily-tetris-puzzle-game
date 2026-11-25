from random import randint

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandParser, CommandError
from django.utils import timezone
from tetris_puzzdle.models import DailyPuzzle, PuzzleAttempt

class Command(BaseCommand):
    help = "Create a daily puzzle and dummy attempts for an existing user."

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "--username",
            required=True,
            help="Username to attach the dummy attempts to.",
        )

    def handle(self, *args, **options):
        puzzle_date = timezone.localdate()
        puzzle, created = DailyPuzzle.objects.get_or_create(
            date=puzzle_date,
            defaults={
                "starting_board": [],
                "piece_sequence": [],
            },
        )
        self.stdout.write(f"Puzzle: {puzzle} (created: {created})")

        User = get_user_model()
        try:
            user = User.objects.get(username=options["username"])
        except User.DoesNotExist:
            raise CommandError(f'No user found with username "{options["username"]}".')

        is_first_attempt = not PuzzleAttempt.objects.filter(
            puzzle=puzzle,
            user=user,
        ).exists()

        for x in range(5):
            attempt = PuzzleAttempt.objects.create(
                puzzle=puzzle,
                user=user,
                score=randint(0, 1000),
                lines_cleared=randint(0,10),
                first_attempt=is_first_attempt,
                day_of=(puzzle.date == puzzle_date),
                submitted_at=timezone.now(),
            )
            print("Added attempt: ", attempt)
            is_first_attempt = False;
