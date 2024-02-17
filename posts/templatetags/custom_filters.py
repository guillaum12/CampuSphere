from django import template
from posts.models import Power  # Import your model
from profiles.models import Profile

register = template.Library()

@register.filter(name='user_post_power')
def user_post_power(post, user):

    profile = Profile.objects.get(user=user)

    try:
        power_object = Power.objects.get(post=post, profile=profile)
        return power_object.power
    except Power.DoesNotExist:
        return None