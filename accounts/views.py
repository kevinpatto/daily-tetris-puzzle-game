from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm
from .models import UserProfile
from django.shortcuts import get_object_or_404, render


def get_user_profile(request, username):
    profile = (UserProfile.objects.select_related("user").filter(user__username=username).first())
    if profile is None:
        return render(request, "profiles/profile.html", {"profile": None, "invalidUsername": username}, status=404)
    else:
        return render(request, 'profiles/profile.html', {"profile": profile})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

## API call for an inputted user's scores.
## format: /api/accounts/<username>
@require_GET
def get_score_by_user(request, username):
    ## find user by username input in API request, 404 if not found to be handled by frontend
    user = get_object_or_404(UserProfile, user__username=username)
    attempts = UserProfile.objects.filter(user=user).order_by("-score")

    ## return as JSON, to be handled in frontend by vite
    return JsonResponse({
        "user": user.username,
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