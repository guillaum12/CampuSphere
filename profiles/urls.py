from django.urls import path
from .views import (invites_received_view, 
                    my_profile_view,  
                    invite_profile_list_view,
                    ProfileListView)

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my_invites/', invites_received_view, name='my-invites-view'),
    path('all_profiles/', ProfileListView.as_view(), name='all-profiles-view'),
    path('to_invite/', invite_profile_list_view, name='invite-profiles-view'),
]
