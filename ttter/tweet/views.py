from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, View

from .forms import TweetForm
from .models import LikeForTweet, Tweet


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweet/tweet_create.html"
    form_class = TweetForm
    success_url = reverse_lazy("tweet:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetListView(LoginRequiredMixin, ListView):
    template_name = "tweet/tweet_list.html"
    model = Tweet
    queryset = Tweet.objects.select_related("user").all().order_by("-created_at")


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweet/tweet_detail.html"
    model = Tweet


class TweetDeleteViwe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweet/tweet_delete.html"
    success_url = reverse_lazy("tweet:home")

    def test_func(self):
        self.object = self.get_object()
        return self.object.user == self.request.user


class LikeView(View, LoginRequiredMixin):
    def post(self, request, *arg, **kwargs):
        user = request.user
        tweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        LikeForTweet.objects.get_or_create(user=user, tweet=tweet)
        likes_count = tweet.likes.count()
        context = {
            "liked_count": likes_count,
            "tweet_id": tweet.id,
            "is_liked": True,
        }

        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *arg, **kwargs):
        user = request.user
        tweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        LikeForTweet.objects.filter(user=user, tweet=tweet).delete()
        context = {
            "liked_count": tweet.likes.count(),
            "tweet_id": tweet.id,
            "is_liked": False,
        }
        return JsonResponse(context)
