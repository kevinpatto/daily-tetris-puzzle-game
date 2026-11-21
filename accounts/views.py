from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm
from .models import UserProfile
from django.shortcuts import get_object_or_404, render

def get_user_profile(request, username):
    user = get_object_or_404(UserProfile, username=username)
    return render(request, 'profiles/profile.html', {"user":user})

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
