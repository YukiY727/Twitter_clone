from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("user_data_input/", views.UserDataInput.as_view(), name="user_data_input"),
    path(
        "user_data_confirm/", views.UserDataConfirm.as_view(), name="user_data_confirm"
    ),
    path("user_data_create/", views.UserDataCreate.as_view(), name="user_data_create"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
