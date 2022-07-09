from django.urls import reverse_lazy

from .forms import TweetForm
from .models import Tweet


class TweetCreateView(CreateView):
    template_name = 'tweet:tweet_create.html'
    form_class = TweetForm
    success_url = reverse_lazy('base:top')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TweetListView(ListView):
    template_name = 'tweet:tweet_list.html'
    model = Tweet
