from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars_html, linebreaks
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
    if args is None:
        return False
    # Diviser les arguments
    max_length, max_lines = [int(arg) for arg in args.split(',')]

    # On ne conserve qu'au maximum max_lines lignes
    res = "\r\n".join(value.split("\r\n")[:max_lines])

    # On tronque le texte à max_length caractères
    res = truncatechars_html(res, max_length)

    # On supprime les lignes vides à la fin
    while res != "":
        last_line = res.split("\r\n")[-1]
        last_line_cleaned = last_line.replace(
            "&nbsp;", "").replace(
            "<p>", "").replace(
            "</p>", "").strip()
        if last_line_cleaned == "":
            res = "\r\n".join(res.split("\r\n")[:-1])
        else:
            break

    return res


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
