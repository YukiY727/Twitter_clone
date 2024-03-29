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
    queryset = User.objects.values_list("username", flat=True)


class UserPage(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_user = self.request.user
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        if request_user != user:
            context["is_followed"] = FriendShip.objects.filter(
                followee=request_user, follower=user
            ).exists()
        context["user"] = user
        context["post_item"] = user.tweet_set.all()
        context["followee_count"] = user.followee.count()
        context["follower_count"] = user.follower.count()
        return context


class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs["username"])
        ctx["followers"] = user.followees.all()
        return ctx


class FollowingListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs["username"])
        ctx["followings"] = user.followers.all()
        return ctx


class FollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follow.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["follower"] = get_object_or_404(User, username=self.kwargs["username"])
        return ctx

    def post(self, *args, **kwargs):
        follower = get_object_or_404(User, username=self.kwargs["username"])
        followee = get_object_or_404(User, id=self.request.user.id)
        if followee == follower:
            messages.warning(self.request, "自分自身はフォローできません。")
            return render(self.request, "accounts/follow.html", {"follower": follower})
        else:
            _, created = FriendShip.objects.get_or_create(
                followee=followee, follower=follower
            )
            if not created:
                messages.warning(self.request, f"{follower.username}さんはすでにフォローしています。")
                return render(
                    self.request, "accounts/follow.html", {"follower": follower}
                )
        return redirect("tweet:home")


class UnFollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/unfollow.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["follower"] = get_object_or_404(User, username=self.kwargs["username"])
        return ctx

    def post(self, *args, **kwargs):
        follower = get_object_or_404(User, username=self.kwargs["username"])
        followee = get_object_or_404(User, id=self.request.user.id)
        if followee == follower:
            messages.warning(self.request, "自分自身のフォロー解除はできません。")
            return render(
                self.request, "accounts/unfollow.html", {"follower": follower}
            )
        if FriendShip.objects.filter(followee=followee, follower=follower).exists():
            FriendShip.objects.filter(followee=followee, follower=follower).delete()
        else:
            messages.warning(self.request, f"{follower.username}さんはフォローしていません。")
            return render(
                self.request, "accounts/unfollow.html", {"follower": follower}
            )
        return redirect("tweet:home")
