from .forms import CommentCreateModelForm, PostCreateModelForm
from .models import Like, Post, Power, Report


def find_post_to_show(sort):

    if sort in {"created", "report_number"}:
        post_to_show = Post.objects.filter(is_post=True).order_by("-" + sort)

    else:
        post_to_show = Post.objects.filter(is_post=True).order_by("-created")

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


def add_comment_if_submitted(request, profile):
    if "submit_c_form" in request.POST:

        # Retrieve the post_id from the form data
        post_id = request.POST.get('post_id', None)
        parent_post = Post.objects.get(id=post_id)

        c_form = CommentCreateModelForm(request.POST)

        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.profile = profile
            instance.post = Post.objects.get(id=request.POST.get("post_id"))
            instance.author = profile
            instance.is_post = False
            instance.in_response_to = parent_post
            instance.save()

            c_form = CommentCreateModelForm()

            return True


def get_post_id_and_post_obj(request):
    post_id = request.POST.get("post_id")
    post_obj = Post.objects.get(id=post_id)
    return post_id, post_obj


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
    
    # Add / remove target profile
    # and create power_added variable
    if profile in post_obj.powered.all():
        # post_obj.powered.remove(profile)
        power_added = False
    else:
        post_obj.powered.add(profile)
        power_added = True

    # Get Power object if post already powered, create Power object if not
    power, created = Power.objects.get_or_create(profile=profile, post_id=post_id)

    power.power = power_amount
    power.save()
    post_obj.save()

    # power_added is used for the power.js script
    return power_added