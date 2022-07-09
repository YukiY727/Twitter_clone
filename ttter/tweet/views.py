from forms import TweetForm


class DiaryCreateView(CreateView):
    template_name = 'diary_create.html'
    form_class = TweetForm
    success_url = reverse_lazy('diary:diary_create_complete')
