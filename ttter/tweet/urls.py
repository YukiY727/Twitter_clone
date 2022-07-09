from django.urls import path
from . import views

app_name = 'tweet'
urlpatterns = [
    path('create/', views.TweetCreateView.as_view(), name='tweet_create'),
    path('list/', views.TweetListView.as_view(), name='tweet_list'),
]