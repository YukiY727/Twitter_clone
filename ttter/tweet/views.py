from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import TweetForm
from .models import Tweet


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


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweet/tweet_detail.html"
    model = Tweet


class TweetDeleteViwe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweet/tweet_delete.html"
    success_url = reverse_lazy("tweet:home")

    def test_func(self):
        if Tweet.objects.filter(pk=self.kwargs["pk"]).exists():
            current_user = self.request.user
            tweet_user = Tweet.objects.get(pk=self.kwargs["pk"]).user
            return current_user == tweet_user
        else:
            return Http404
