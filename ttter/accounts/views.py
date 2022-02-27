from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

# Create your views here.
User = get_user_model()

class SignUpFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserCreateView(FormView):
    form_class = SignUpFrom
    template_name = 'accounts/create.html'
    success_url = reverse_lazy('base:top')

    def form_valid(self, form):
        if self.request.POST['next'] == 'back':
            return render(self.request, 'accouts/create.html',
                          {'form': form})
        elif self.request.POST['next'] == 'confirm':
            return render(self.request, 'accounts/create_confirm.html',
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
