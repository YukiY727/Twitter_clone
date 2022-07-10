from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import SignUpFrom

# Create your views here.
User = get_user_model()


class UserDataInput(FormView):
    template_name = "accounts/create.html"
    form_class = SignUpFrom

    def form_valid(self, form):
        return render(self.request, "accounts/create.html", {"form": form})


class UserDataConfirm(FormView):
    form_class = SignUpFrom

    def form_valid(self, form):
        return render(self.request, "accounts/create_confirm.html", {"form": form})

    def form_invalid(self, form):
        return render(self.request, "accounts/create.html", {"form": form})


class UserDataCreate(CreateView):
    form_class = SignUpFrom
    success_url = reverse_lazy("tweet:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response

    def form_invalid(self, form):
        return render(self.request, "accounts/create.html", {"form": form})
