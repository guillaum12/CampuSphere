from urllib import request

from convention.utils import send_email
from .forms import CommentCreateModelForm, PostCreateModelForm
from .models import Like, Post, Power, Report, Choice
from profiles.views_utils import get_request_user_profile
from django.template.loader import render_to_string
from django.middleware.csrf import get_token


def filter_by_new_posts(post_to_show, user):
    profile = get_request_user_profile(user)
    return [post for post in post_to_show if profile not in post.powered.all()]


def find_post_to_show(user, filter_form):

    post_to_show = Post.objects.filter(is_post=True).order_by('-created')

    if filter_form.is_valid():
        # Filter by quality

        filter_option = filter_form.cleaned_data.get('filter_option')

        if user.is_staff and filter_option == 'reported':
            post_to_show = Post.objects.order_by_report_number()

        elif filter_option == 'votedpercentage':
            post_to_show = Post.objects.order_by_progress()

        elif filter_option == 'many':
            post_to_show = Post.objects.order_by_voter_number()

        elif filter_option == 'favorite':
            post_to_show = Post.objects.get_all_favorite_posts(user=user)
            
        else:
            post_to_show = Post.objects.order_by_score_pondere()

        # Filter by new posts
        new_posts = filter_form.cleaned_data.get('new_posts')

        if new_posts:
            post_to_show = filter_by_new_posts(post_to_show, user)

        # Filter by theme
        theme = filter_form.cleaned_data.get('themes')

        if theme not in '- ':
            theme_obj = Choice.objects.get(theme_name=theme)
            post_to_show = [post for post in post_to_show if post.theme == theme_obj]

        campus = filter_form.cleaned_data.get('campus')

        if campus not in '- ':
            post_to_show = [post for post in post_to_show if post.campus == campus]

        return post_to_show


def add_post_if_submitted(request, profile):
    if "submit_p_form" in request.POST:

        p_form = PostCreateModelForm(request.POST, request.FILES)

        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.is_post = True
            instance.save()

            p_form = PostCreateModelForm()

            return True


def add_comment_if_submitted(request, parent_post, parent_proposition, profile, content):
    new_comment = Post()
    new_comment.author = profile
    new_comment.is_post = False
    new_comment.content = content

    new_comment.in_response_to = parent_post

    new_comment.save()

    comment_id = new_comment.id
    csrf_token = get_token(request)

    if comment_id:
        comment_html = render_to_string(
            "posts/single_comment.html",
            {"comment": Post.objects.get(id=comment_id),
                "user": profile.user,
                "post": Post.objects.get(id=parent_proposition.id),
                "csrf_token": csrf_token,
                "request": request}
        )
        return comment_html


def send_mail_when_commented(parent_post, parent_proposition, comment_content):
        
    post_author = parent_post.author
    post_author_email = post_author.user.email

    user_profile = get_request_user_profile(request.user)
    
    message = render_to_string("posts/email_templates/email_new_comment.html", {
        'comment_content': comment_content,
        'parent_post': parent_post,
        'parent_proposition': parent_proposition,
        
    })
    
    if post_author != user_profile:
        send_email(request, "Nouveau commentaire", message, post_author_email)


def get_post_id_and_post_obj(request):
    post_id = request.POST.get("post_id")
    post_obj = Post.objects.get(id=post_id)
    return post_id, post_obj


def get_theme_path_from_theme(request, theme):
    current_theme = theme
    if not current_theme:
        return ["Divers"]
    theme_path = [current_theme.theme_name]
    while current_theme.parent_categorie:
        current_theme = current_theme.parent_categorie
        theme_path.insert(0, current_theme.theme_name)
    return theme_path


def like_unlike_post(profile, post_id, post_obj):

    # Add / remove target profile
    # from liked field in post_obj
    # and create like_added variable
    if profile in post_obj.liked.all():
        post_obj.liked.remove(profile)
        like_added = False
    else:
        post_obj.liked.add(profile)
        like_added = True

    # Get Like object if post already liked, create Like object if not
    like, created = Like.objects.get_or_create(profile=profile, post_id=post_id)

    # If Like object wasnt created
    # by get_or_create function - delete
    if not created:
        like.delete()
    # Else - save Like object
    else:
        like.save()
        post_obj.save()

    # like_added is used for the like.js script
    return like_added


def never_display_explanations(profile):
    try:
        profile.display_site_explanation = False
        profile.save()
        return True
    except Exception as e:
        print("Une erreur est survenue au moment de cacher définitivement les explications du site à la connexion", e)
        return False


def report_unreport_post(profile, post_id, post_obj):
    # Add / remove target profile
    # from reported field in post_obj
    # and create report_added variable
    if profile in post_obj.reported.all():
        post_obj.reported.remove(profile)
        report_added = False
    else:
        post_obj.reported.add(profile)
        report_added = True

    # Get report object if post already reported, create Report object if not
    report, created = Report.objects.get_or_create(profile=profile, post_id=post_id)

    # If report object wasnt created
    # by get_or_create function - delete
    if not created:
        report.delete()
    # Else - save report object
    else:
        report.save()
        post_obj.save()

    # report_added is used for the report.js script
    return report_added


def power_post(profile, post_id, post_obj, power_amount):
    power, created = Power.objects.get_or_create(profile=profile, post_id=post_id)
    if created:
        post_obj.powered.add(profile)
        post_obj.save()

    # On vérifie si l'utilisateur a déjà donné la même note à cette proposition
    if not created and power.power == power_amount:
        power_added = False
        post_obj.powered.remove(profile)
        power.delete()
        post_obj.save()
    else:
        power_added = True
        power.power = power_amount
        power.save()

    # power_added is used for the power.js script
    return power_added


def like_unlike_comment(profile, comm_id, comm_obj, like_value):
    power, created = Power.objects.get_or_create(profile=profile, post_id=comm_id)
    if created:
        print("like créé")
        comm_obj.powered.add(profile)
        comm_obj.save()
    # On vérifie si l'utilisateur a déjà donné la même note à cette proposition
    if not created and power.power == like_value:
        print("same note")
        power_added = False
        comm_obj.powered.remove(profile)
        power.delete()
        comm_obj.save()
    else:
        print("new different note")
        power_added = True
        power.power = like_value
        power.save()

    # power_added is used for the power.js script
    return power_added
