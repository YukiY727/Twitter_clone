
from django.views.generic import TemplateView


class TopView(TemplateView):
    template_name = 'base/top.html'
