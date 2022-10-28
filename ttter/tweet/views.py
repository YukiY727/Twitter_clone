from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    queryset = Tweet.objects.select_related('user').all().order_by("-created_at")


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
