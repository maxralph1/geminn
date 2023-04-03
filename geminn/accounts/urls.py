from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
# from .forms import PasswordResetConfirmForm, CustomPasswordResetForm, UserLoginForm

app_name = 'accounts'

urlpatters = [
    # path('login/', auth_views.LoginView.as_view()
]
