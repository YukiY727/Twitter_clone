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
    path("<int:user_id>/user_page/", views.UserPage.as_view(), name="user_page"),
    path(
        "<int:user_id>/following_list/",
        views.FollowingListView.as_view(),
        name="following_list",
    ),
    path(
        "<int:user_id>/follower_list/",
        views.FollowerListView.as_view(),
        name="follower_list",
    ),
    path("<int:user_id>/follow/", views.FollowView.as_view(), name="follow"),
    path("userlist/", views.UserListView.as_view(), name="userlist"),
    path("<int:user_id>/unfollow/", views.UnFollowView.as_view(), name="unfollow"),
]
