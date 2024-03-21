from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars_html, striptags
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


@register.filter(name='shorten_text')
def shorten_text(value, args):
    # On récupère les arguments
    max_chars_by_line, max_lines = args.split(",")
    max_chars_by_line = int(max_chars_by_line)
    max_lines = int(max_lines)
    result = ""

    # On compte le nombre de lignes
    lines = value.split("\r\n")
    remaining_chars = max_chars_by_line * max_lines
    nb_remaining_lines = max_lines
    for line in lines:
        if remaining_chars < 0 or nb_remaining_lines <= 0:
            break
        # On retire les balises vides
        if striptags(line) == "":
            continue
        result += truncatechars_html(line, remaining_chars)
        remaining_chars -= len(striptags(truncatechars_html(line, remaining_chars)))
        nb_remaining_lines -= 1

    return result


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def to_int(value):
    # Remplace les virgules en points
    return int(value)
