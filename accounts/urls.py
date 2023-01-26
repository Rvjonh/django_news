from django.urls import path
from .views import SignUpView, CustomUserUpdateView, Password_reset_request

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("update/<int:pk>/", CustomUserUpdateView.as_view(), name="user_update"),
    path("password_reset/", Password_reset_request, name="password_reset"),
]
