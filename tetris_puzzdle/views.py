from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET

from datetime import datetime
from .models import *


# most of this file was AI generated using duck.ai with model GPT-6 Luna
## from here on out,  i added in comments, denoted by "##", to explain what is happening (for myself mostly)

## for use in finding a leaderboard for url path
def find_leaderboard(request, date):
    ## parses url ./leaderboard/<date> for date, returning None if invalid url format
    puzzle_date = parse_date(date)

    ## 404 if the URL's date input is an invalid input
    if puzzle_date is None:
        return render(
            request,
            "leaderboard.html",
            {"leaderboard": None, "valid_input": False},
            status=404,
        )

    ## check if puzzle with URL's date exists
    puzzle_exists = DailyPuzzle.objects.filter(date=puzzle_date).exists()
    ## sends info for page to handle if that URL's date does not exist
    if not puzzle_exists:
        return render(
            request,
            "leaderboard.html",
            {"leaderboard": None, "valid_input": True, "date": date},
            status=404,
        )

    ## order does not really matter
    leaderboard = (
        PuzzleAttempt.objects
        .filter(puzzle__date=puzzle_date)
        .select_related("user")
        .order_by("-score", "pk")
    )

    ## returns the leaderboard's information for the page to use in title
    return render(
        request,
        "leaderboard.html",
        {
            "leaderboard": leaderboard,
            "is_leaderboard": True,
            "date": date,
        },
    )


## get_leaderboard works as an API call for vite
## essentially, this will get called anytime after a user changes a filter. django handles the sorting and filtering, vite handles the rendering
@require_GET
def get_leaderboard(request, date, ):
    ## get puzzle by YYYY-MM-DD format, return error if invalid input
    try:
        puzzle_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Date must use YYYY-MM-DD format."}, status=400)

    ## find puzzle by date or 404 if no puzzle exists for date, to be handled by frontend
    puzzle = get_object_or_404(DailyPuzzle, date=puzzle_date)
    ## get all attempts at puzzle, start with every attempt
    attempts = PuzzleAttempt.objects.filter(puzzle=puzzle)

    ## these next two if statements allow for the request to filter based on attributes we made
    ## filter only for first attempts
    if request.GET.get("first_attempt") == "1":
        attempts = attempts.filter(first_attempt=True)

    ## filter only for attempts on the day of
    if request.GET.get("day_of") == "1":
        attempts = attempts.filter(day_of=True)

    mode = request.GET.get("mode", "all")

    ## get only a user's best attempt (within our filters)
    if mode == "best":
        # Keep each player's highest-scoring matching attempt.
        attempts = (
            attempts
            .annotate(
                ## uses Window to divide attempts into groups by the player who made them
                player_rank=Window(
                    expression=RowNumber(),
                    partition_by=[F("user_id")],
                    order_by=[F("score").desc(), F("pk").asc()],
                )
            )
            .filter(player_rank=1)
            ## uses the Window and asks only for the first attempt, which will be the best due to sorting
        )
    elif mode not in {"all"}:  ## error if invalid input
        return JsonResponse(
            {"error": "mode must be 'best', or 'all'."},
            status=400,
        )

    ## return as JSON, to be handled in frontend by vite
    return JsonResponse({
        "date": puzzle_date.isoformat(),
        "mode": mode,
        "attempts": [
            {
                "username": attempt.user.username,
                "score": attempt.score,
                "lines_cleared": attempt.lines_cleared,
                "first_attempt": attempt.first_attempt,
                "day_of": attempt.day_of,
            }
            for attempt in attempts
        ],
    })
