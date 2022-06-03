from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import SignUpFrom

# Create your views here.
User = get_user_model()


class UserDataInput(FormView):
    """ユーザー情報の入力

    このビューが呼ばれるのは、以下の2箇所です。
    ・初回の入力欄表示(aタグでの遷移)
    ・確認画面から戻るを押した場合(これはPOSTで飛んできます)

    初回の入力欄表示の際は、空のフォームをuser_data_input.htmlに渡し、
    戻る場合は、POSTで飛んできたフォームデータをそのままuser_data_input.htmlに渡します。

    """
    template_name = 'accounts/create.html'
    form_class = SignUpFrom

    def form_valid(self, form):
        return render(self.request, 'accounts/create.html',
                      {'form': form})


class UserDataConfirm(FormView):
    """ユーザー情報の確認

    ユーザー情報入力後、「送信」を押すとこのビューが呼ばれます。(create.htmlのform action属性がこのビュー)
    データが問題なければcreate_confirm.html(確認ページ)を、入力内容に不備があればcreate.html(入力ページ)に
    フォームデータを渡します。

    """
    form_class = SignUpFrom

    def form_valid(self, form):
        return render(self.request, 'accounts/create_confirm.html',
                      {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'accounts/create.html',
                      {'form': form})


class UserDataCreate(CreateView):
    """ユーザーデータの登録ビュー。ここ以外では、CreateViewを使わないでください"""
    form_class = SignUpFrom
    success_url = reverse_lazy('base:top')

    def from_valid(self, form):
        return redirect(self.success_url)

    def form_invalid(self, form):
        """基本的にはここに飛んでこないはずです。UserDataConfrimでバリデーションは済んでるため"""
        return render(self.request, 'accounts/create.html',
                      {'form': form})
