from urllib import request
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, ListView

from .forms import SignUpFrom
from .models import FriendShip
from tweet.models import Tweet
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
    template_name = 'accounts/user_list.html'
    model = User
    
    def get_queryset(self):
        return User.objects.all()


class UserPage(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user_page.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_user = self.request.user
        print(self.kwargs ,1111111111111111111) 
        user = get_object_or_404(User, id=self.kwargs.get("user_id"))
        post_item = Tweet.objects.filter(user=user)
        context["is_followed"] = FriendShip.objects.filter(follower=request_user, followee=user).exists()
        print(FriendShip.objects.filter(followee=request_user, follower=user).exists())
        context["request_user"] = request_user
        context["user"] = user
        context["post_item"] = post_item
        return context

    # def get_queryset(self, **kwargs):
    #     context = super().get_queryset(**kwargs)
    #     print(type(self.request.user.id))
    #     print(context)
    #     return User.objects.get(id=int(context['username']))

    # def get_queryset(self):
    #     return User.objects.get(id=self.request.user.id)


class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        print(self.kwargs ,1111111111111111111)
        print(FriendShip.objects.filter(follower_id=self.kwargs.get("user_id")))
        ctx["followers"] = FriendShip.objects.filter(follower_id=self.kwargs.get("user_id"))

        return ctx
# class UserFolloweeList(LoginRequiredMixin, TemplateView):
#     template_name = "accounts/user_follow_list.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["followee"] = get_object_or_404(User, id=self.kwargs.get("username"))
#         print(**kwargs)
#         print(self.kwargs.get("username"))
#         return context
    
class FollowingListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        print(self.kwargs)
        print(self.kwargs.get("user_id"))
        print(FriendShip.objects.filter(followee=self.kwargs.get("user_id")))
        ctx["followings"] = FriendShip.objects.filter(followee=self.kwargs.get("user_id"))
        return ctx
class FollowView(LoginRequiredMixin, TemplateView):
    # template_name = "accounts/follow.html"
    template_name = "accounts/follow.html"
    model = FriendShip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.follower = get_object_or_404(User, user=self.kwargs["user_id"])
        self.followee = get_object_or_404(User, id=self.request.user.id)
        context['follower'] = self.follower
        if self.followee == self.follower:
            messages.warning(self.request, "自分自身はフォローできません。")
        elif FriendShip.objects.filter(followee=self.followee, follower=self.follower).exists():
            messages.warning(self.request, f"{self.follower.username}さんはすでにフォローしています。")
        return context

    def post(self, **kwargs):
        FriendShip.objects.create(followee=self.followee, follower=self.follower)
        return HttpResponseRedirect(reverse_lazy("tweet:home"))


# class FollowView(UserMixin, TemplateView):
#     template_name = "accounts/follow.html"


#     def post(self, request, *args, **kwargs):
#         user, target = request.user, self.get_target()
#         kwargs.setdefault("errors", [])
#         if user.pk == target.pk:
#             kwargs["errors"].append("自分自身のフォローはできません。")
#         elif FriendShip.objects.filter(follower=user, followee=target).exists():
#             kwargs["errors"].append(f"{target.username}は既にフォローしています。")
#         else:
#             FriendShip.objects.create(follower=user, followee=target)
#             return redirect("accounts:home")
#         return self.get(request, *args, **kwargs)

class UnFollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/unfollow.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.follower = get_object_or_404(User, user=self.kwargs["user_id"])
        self.followee = get_object_or_404(User, id=self.request.user.id)
        context['follower'] = self.follower
        if self.followee == self.follower:
            messages.warning(self.request, "無効な操作です。")
        return context

    def post(self, **kwargs):
        if FriendShip.objects.filter(followee=self.followee, follower=self.follower).exists():
            FriendShip.objects.filter(followee=self.followee, follower=self.follower).delete()
            return HttpResponseRedirect(reverse_lazy("accounts:home"))
