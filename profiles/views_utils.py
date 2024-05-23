from django.shortcuts import redirect

from .forms import ProfileModelForm
from .models import Profile


def get_request_user_profile(request_user):
    user = Profile.objects.get(user=request_user)
    return user


def get_profile_form_by_request_method(request, profile):
    if request.method == "POST":
        form = ProfileModelForm(request.POST, request.FILES, instance=profile)
    else:
        form = ProfileModelForm(instance=profile)
    return form


def get_profiles_by_users_list(users):
    result = [Profile.objects.get(user=user) for user in users]
    return result


def check_if_friends(profile, request_user):
    """
    Returns true if request user is in profile's friends
    and vice versa
    """
    return request_user in profile.friends.all()


def get_friends_of_user(user):
    request_user_profile = Profile.objects.get(user=user)
    friends_users = request_user_profile.friends.all()
    friends_profiles = get_profiles_by_users_list(friends_users)
    return friends_profiles


def get_profile_by_pk(request):
    pk = request.POST.get("pk")
    profile = Profile.objects.get(pk=pk)
    return profile



def follow_unfollow(my_profile, profile):
    """
    Checks if profile in my_profile's followers,
    if so - removes profile from my_profile's followers,
    else - adds profile to my_profile's followers
    """
    if profile.user in my_profile.following.all():
        my_profile.following.remove(profile.user)
        profile.followers.remove(my_profile.user)
    else:
        my_profile.following.add(profile.user)
        profile.followers.add(my_profile.user)


def redirect_back(request):
    return redirect(request.META.get("HTTP_REFERER", "/"))

