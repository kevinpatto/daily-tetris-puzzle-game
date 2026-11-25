from django.conf import settings
from django.db import models
# most of this file was AI generated using duck.ai with model GPT-6 Luna
## from here on out,  i added in comments, denoted by "##", to explain what is happening (for myself mostly)

## model for daily puzzles.
class DailyPuzzle(models.Model):
    date = models.DateField(unique=True) ## unique date of puzzle, every day can only have one puzzle
    starting_board = models.JSONField(default=list) ## setup of puzzle as JSON
    piece_sequence = models.JSONField(default=list) ## piece sequence as JSON
    created_at = models.DateTimeField(auto_now_add=True) ## time puzzle was created

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Puzzdle for {self.date}"

## model for puzzle attempts
## attached to a puzzle, as well as a user
## used for display on a user's profile and as
class PuzzleAttempt(models.Model):
    puzzle = models.ForeignKey(
        DailyPuzzle,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="puzzle_attempts",
    )
    day_of = models.BooleanField(default=False) ## if attempt started on day of puzzle
    first_attempt = models.BooleanField(default=False) ## if attempt is the first a user made
    score = models.PositiveIntegerField(default=0) ## tetris score for attempt
    lines_cleared = models.PositiveIntegerField(default=0) ## number of lines cleared
    started_at = models.DateTimeField(auto_now_add=True) ## time puzzle was started
    submitted_at = models.DateTimeField(null=True, blank=True) ## time puzzle submitted
    completed = models.BooleanField(default=False) ## if puzzle is in completed state
    current_board = models.JSONField(default=list) ## saves board state for later if incomplete
    sequence_count = models.PositiveIntegerField(default=0) ## saves place in sequence for later if incomplete

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user} — {self.puzzle.date} — {self.score}"