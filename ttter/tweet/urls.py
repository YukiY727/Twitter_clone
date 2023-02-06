from django.urls import path

from . import views

app_name = "tweet"
urlpatterns = [
    path("create/", views.TweetCreateView.as_view(), name="tweet_create"),
    path("", views.TweetListView.as_view(), name="home"),
    path("detail/<uuid:pk>/", views.TweetDetailView.as_view(), name="tweet_detail"),
    path("delete/<uuid:pk>/", views.TweetDeleteViwe.as_view(), name="tweet_delete"),
    path("like/<uuid:pk>/", views.LikeView.as_view(), name="like"),
    path("unlike/<uuid:pk>/", views.UnlikeView.as_view(), name="unlike"),
]
