from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import SignUpView,  get_user_profile

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
