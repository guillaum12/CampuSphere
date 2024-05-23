from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from posts.forms import CommentCreateModelForm
from posts.models import Post

from .models import Profile
from .views_utils import (
    check_if_friends,
    follow_unfollow,
    get_friends_of_user,
    get_profile_by_pk,
    get_request_user_profile,
    redirect_back,
)


# Function-based views
@login_required
def show_profile_view(request, id):
    """
    Shows profile by pk.
    View url: /profiles/show_profile/<int:id>/
    """
    # Check if profile id is current user's id and url is /profiles/show_profile/<int:id>/
    if id == request.user.id and request.path == f"/profiles/show_profile/{id}/":
        return redirect("profiles:my-profile-view")

    profile = get_object_or_404(Profile, id=id)

    context = {
        "profile": profile,
    }

    return render(request, "profiles/show_profile.html", context)


@login_required
def my_profile_view(request):
    """
    Shows request's user profile.
    View url: /profiles/myprofile/
    """
    profile = get_request_user_profile(request.user)
    return show_profile_view(request, profile.id)


@login_required
def toggle_ban_view(request, profile_id):
    """
    Toggles profile user ban status.
    View url: /profiles/toggle_ban/<int:profile_id>/
    """
    profile = Profile.objects.get(id=profile_id)
    profile.is_banned = not profile.is_banned
    profile.save()

    return redirect_back(request)


@login_required
def received_invites_view(request):
    """
    Shows request's user received invites.
    View url: /profiles/received_invites/
    """
    profile = get_request_user_profile(request.user)
    profiles = get_received_invites(profile)

    context = {
        "profiles": profiles,
    }

    return render(request, "profiles/received_invites.html", context)


@login_required
def sent_invites_view(request):
    """
    Shows request's user sent invites.
    View url: /profiles/sent_invites/
    """
    profile = get_request_user_profile(request.user)
    profiles = get_sent_invites(profile)

    context = {
        "profiles": profiles,
    }

    return render(request, "profiles/sent_invites.html", context)


@login_required
def switch_follow(request):
    """
    Follows/unfollows user by pk.
    View url: /profiles/switch_follow/
    """
    if request.method == "POST":
        my_profile = get_request_user_profile(request.user)
        profile = get_profile_by_pk(request)

        follow_unfollow(my_profile, profile)

    return redirect_back(request)


@login_required
def accept_invitation(request):
    """
    Accepts invitation from user by pk.
    View url: /profiles/received_invites/accept/
    """
    if request.method == "POST":
        sender = get_profile_by_pk(request)
        receiver = get_request_user_profile(request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == "sent":
            rel.status = "accepted"
            rel.save()

    return redirect_back(request)


@login_required
def reject_invitation(request):
    """
    Rejects (deletes) invitation from user by pk.
    View url: /profiles/received_invites/reject/
    """
    if request.method == "POST":
        sender = get_profile_by_pk(request)
        receiver = get_request_user_profile(request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == "sent":
            rel.delete()

    return redirect_back(request)


@login_required
def my_friends_view(request):
    """
    Shows request's user friends.
    View url: /profiles/my_friends/
    """
    profile = get_request_user_profile(request.user)
    following = profile.following.all()

    profiles = Profile.objects.get_my_friends_profiles(request.user)

    context = {
        "following": following,
        "profiles": profiles,
    }

    return render(request, "profiles/my_friends.html", context)


@login_required
def search_profiles(request):
    """
    Searches for profiles by their username.
    View url: /profiles/search/
    """
    search = request.GET.get("q", "")
    profiles = Profile.objects.filter(user__username__icontains=search)

    context = {
        "search": search,
        "profiles": profiles,
    }

    if search:
        return render(request, "profiles/search_profiles.html", context)

    return render(request, "profiles/search_profiles.html")


@login_required
def send_invitation(request):
    """
    Creates a "sent" relationship between request's profile
    and target profile.
    View url: /profiles/send-invite/
    """
    if request.method == "POST":
        sender = get_request_user_profile(request.user)
        receiver = get_profile_by_pk(request)

        Relationship.objects.create(
            sender=sender,
            receiver=receiver,
            status="sent",
        )

    return redirect_back(request)


@login_required
def remove_friend(request):
    """
    Deletes relationship between request's profile and target profile.
    View url: /profiles/remove-friend/
    """
    if request.method == "POST":
        sender = get_request_user_profile(request.user)
        receiver = get_profile_by_pk(request)

        # Find relationship
        # where sender is request's profile and receiver is target profile
        # or where sender is target profile and receiver is request's profile,
        # then delete it
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver))
            | (Q(sender=receiver) & Q(receiver=sender)),
        )
        rel.delete()

    return redirect_back(request)


# Class-based views


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Shows target profile and it's details.
    View url: /profiles/users/<slug>/
    """

    model = Profile
    template_name = "profiles/profile_detail.html"
    form_class = CommentCreateModelForm

    def get(self, request, *args, **kwargs):

        # Redirect to profiles/myprofile/
        # if request's user == target user
        if Profile.objects.get(user=self.request.user) == self.get_object():
            return redirect("profiles:my-profile-view")

        # Default BaseDetailView.get parameters
        # (this has to be here)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        # Add comment form
        form = self.form_class(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = get_request_user_profile(self.request.user)
            instance.post = Post.objects.get(id=request.POST.get("post_id"))
            instance.save()

            form = CommentCreateModelForm()

            return redirect_back(self.request)

    def get_object(self):
        slug = self.kwargs.get("slug")
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_request_user_profile(self.request.user)
        following = profile.following.all

        invited_users, incoming_invite_users = get_relationship_users(profile)

        context["invited_users"] = invited_users
        context["incoming_invite_users"] = incoming_invite_users
        context["following"] = following
        context["form"] = self.form_class

        context["profile"] = self.get_object()
        context["request_user_profile"] = profile

        context["posts"] = self.get_object().posts.all()

        return context


class ProfileListView(LoginRequiredMixin, ListView):
    """
    Shows list of all profiles except request's user.
    View url: /profiles/
    """

    model = Profile
    template_name = "profiles/profile_list.html"

    def get_queryset(self):
        qs = Profile.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.get(user=self.request.user)
        following = profile.following.all

        invited_users, incoming_invite_users = get_relationship_users(profile)

        context["invited_users"] = invited_users
        context["incoming_invite_users"] = incoming_invite_users
        context["following"] = following
        context["profiles"] = self.get_queryset()

        return context


class MessengerListView(LoginRequiredMixin, ListView):
    """
    Shows list of all profiles except request's user.
    View url: /profiles/messenger/
    """

    model = Profile
    template_name = "profiles/messenger.html"

    def get_queryset(self):
        qs = get_friends_of_user(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profiles"] = self.get_queryset()

        return context
