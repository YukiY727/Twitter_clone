from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

# Create your views here.


class UserCreateView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/create.html'
    success_url = reverse_lazy('base:top')

    def form_valid(self, form):
        if self.request.POST['next'] == 'back':
            return render(self.request, 'registration/create.html',
                          {'form': form})
        elif self.request.POST['next'] == 'confirm':
            return render(self.request, 'registration/create_confirm.html',
                          {'form': form})
        elif self.request.POST['next'] == 'regist':
            form.save()
            # 認証
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            # ログイン
            login(self.request, user)
            return super().form_valid(form)
        else:
            # 通常このルートは通らない
            return redirect(reverse_lazy('base:top'))
