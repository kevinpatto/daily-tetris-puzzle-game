from django.contrib.auth.views import LoginView
from django.urls import path
from .views import SignUpView,  get_user_profile
from django.views.generic.base import TemplateView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("<str:username>/", get_user_profile, name="profile"),
]
