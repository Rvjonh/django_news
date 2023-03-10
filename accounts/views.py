from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings


# Create your views here.
from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = (
        "username",
        "email",
        "age",
    )
    success_url = reverse_lazy("home")
    template_name = "registration/update.html"


def Password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        "domain": settings.ALLOWED_HOSTS[0],
                        "site_name": "Newspaper - Rvjonh",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/password_reset/done/")

    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="registration/password_reset_form.html",
        context={"password_reset_form": password_reset_form},
    )
