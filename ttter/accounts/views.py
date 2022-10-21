from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, TemplateView
from tweet.models import Tweet

from .forms import SignUpFrom
from .models import FriendShip

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


class UserListView(LoginRequiredMixin, ListView):
    template_name = "accounts/user_list.html"
    model = User

    def get_queryset(self):
        return User.objects.values_list("username", flat=True)


class UserPage(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_user = self.request.user
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        post_item = Tweet.objects.filter(user=user)
        context["is_followed"] = FriendShip.objects.filter(
            followee=request_user, follower=user
        ).exists()
        context["request_user"] = request_user
        context["user"] = user
        context["post_item"] = post_item
        context["followee_count"] = user.followee.count()
        context["follower_count"] = user.follower.count()
        return context


class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self.user = get_object_or_404(User, username=self.kwargs["username"])

        ctx["followers"] = [
            follower.followee
            for follower in FriendShip.objects.select_related("follower").filter(
                follower=self.user
            )
        ]
        return ctx


class FollowingListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self.user = get_object_or_404(User, username=self.kwargs["username"])
        ctx["followings"] = [
            follower.follower
            for follower in FriendShip.objects.select_related("followee").filter(
                followee=self.user
            )
        ]
        return ctx


class FollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follow.html"
    model = FriendShip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.follower = get_object_or_404(User, username=self.kwargs["username"])
        self.followee = get_object_or_404(User, id=self.request.user.id)
        context["follower"] = self.follower
        if self.followee == self.follower:
            messages.warning(self.request, "自分自身はフォローできません。")
        elif FriendShip.objects.filter(
            followee=self.followee, follower=self.follower
        ).exists():
            messages.warning(self.request, f"{self.follower.username}さんはすでにフォローしています。")
        return context

    def post(self, *args, **kwargs):
        self.follower = get_object_or_404(User, username=self.kwargs["username"])
        self.followee = get_object_or_404(User, id=self.request.user.id)
        if self.followee == self.follower:
            messages.warning(self.request, "自分自身はフォローできません。")
        else:
            _, created = FriendShip.objects.get_or_create(
                followee=self.followee, follower=self.follower
            )
            if not created:
                messages.warning(self.request, f"{self.follower.username}さんはすでにフォローしています。")
        return redirect("tweet:home")


class UnFollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/unfollow.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.follower = get_object_or_404(User, username=self.kwargs["username"])
        self.followee = get_object_or_404(User, id=self.request.user.id)
        context["follower"] = self.follower
        if self.followee == self.follower:
            messages.warning(self.request, "無効な操作です。")
        return context

    def post(self, *args, **kwargs):
        self.follower = get_object_or_404(User, username=self.kwargs["username"])
        self.followee = get_object_or_404(User, id=self.request.user.id)
        if self.followee == self.follower:
            messages.warning(self.request, "自分自身のフォロー解除はできません。")
        if FriendShip.objects.filter(
            followee=self.followee, follower=self.follower
        ).exists():
            FriendShip.objects.filter(
                followee=self.followee, follower=self.follower
            ).delete()
        else:
            messages.warning(self.request, f"{self.follower.username}さんはフォローしていません。")
        return redirect("tweet:home")
