from distutils.dist import command_re
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from django.core.mail import send_mail, EmailMessage, get_connection
from convention import settings
from profiles.views_utils import get_request_user_profile, redirect_back
from django.template.loader import render_to_string

from .forms import PostCreateModelForm, PostFilterForm
from .models import Post, Feedback
from .views_utils import (
    add_comment_if_submitted,
    add_post_if_submitted,
    get_post_id_and_post_obj,
    like_unlike_post,
    power_post,
    find_post_to_show,
    report_unreport_post,
)


# Function-based views


@login_required
def show_first_posts(request):
    """
    Shows first 10 posts.
    View url: /posts/
    """
    return show_selected_posts(request, 0)


@login_required
def show_selected_posts(request, first_post_to_show):
    """
    Shows all posts considering the filters.
    View url: /posts/
    """
    # qs = Post.objects.get_related_posts(user=request.user)

    filter_form = PostFilterForm(request.GET)

    post_to_show = find_post_to_show(
        request.user, filter_form, first_post=first_post_to_show
    )

    profile = get_request_user_profile(request.user)

    if not profile.is_banned:
        if add_post_if_submitted(request, profile):
            return redirect_back(request)

        if add_comment_if_submitted(request, profile):
            return redirect_back(request)
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "You are banned",
        )

    next_first_post_to_show = first_post_to_show + 10

    context = {
        "post_to_show": post_to_show,
        "profile": profile,
        "p_form": PostCreateModelForm(),
        "filter_form": filter_form,
        "next_first_post_to_show": next_first_post_to_show,
    }

    return render(request, "posts/main.html", context)


@login_required
def feedback(request):

    if request.method == "POST":
        feedback = request.POST.get("feedback")
        profile = get_request_user_profile(request.user)
        Feedback.objects.create(author=profile, content=feedback)

        messages.add_message(
            request,
            messages.SUCCESS,
            "Feedback sent successfully!",
        )

    return render(request, "posts/retours.html")


@login_required
def show_post(request, pk):
    """
    Shows a post by pk.
    View url: /posts/<pk>/show/
    """

    context = {
        "post": Post.objects.get(pk=pk),
        "profile": get_request_user_profile(request.user),
    }

    return render(request, "posts/show_post.html", context)


# ________________________________ ASYNCRONOUS ACTIONS ________________________________ #


@login_required
def comment_view(request):
    """
    Adds a comment to a post.
    View url: /posts/comment/
    """
    if request.method == "POST":
        profile = get_request_user_profile(request.user)
        comment_html = add_comment_if_submitted(request, profile)

        if comment_html:
            return JsonResponse({'comment_html': comment_html})

    return JsonResponse({"error": "error"})


@login_required
def switch_like(request):
    """
    Adds/removes like to a post.
    View url: /posts/like/
    """
    if request.method == "POST":
        post_id, post_obj = get_post_id_and_post_obj(request)
        profile = get_request_user_profile(request.user)

        like_added = like_unlike_post(profile, post_id, post_obj)
    else:
        like_added = False
    # Return JSON response for AJAX script in like.js
    return JsonResponse(
        {"like_added": like_added},
    )


@login_required
def switch_report(request):
    """
    Adds/removes report to a post.
    View url: /posts/report/
    """
    if request.method == "POST":
        post_id, post_obj = get_post_id_and_post_obj(request)
        profile = get_request_user_profile(request.user)

        report_added = report_unreport_post(profile, post_id, post_obj)

        # Return JSON response for AJAX script in report.js
        return JsonResponse(
            {
                "status": "success",
                "report_added": report_added,
                "report_number": post_obj.report_number,
            },
        )

    else:
        report_added = False
        return JsonResponse({"error": "error"})


@login_required
def power(request):
    """
    Adpat power of a post.
    View url: /posts/power/
    """
    if request.method == "POST":
        post_id, post_obj = get_post_id_and_post_obj(request)
        profile = get_request_user_profile(request.user)
        power_amount = request.POST.get("power_amount")
        power_added = power_post(profile, post_id, post_obj, power_amount)

        # Return JSON response for AJAX script in power.js
        return JsonResponse(
            {
                "post_progress": post_obj.progress,
                "voter_number": post_obj.voter_number,
                "power_added": power_added,
                "post_color": post_obj.get_color_progress,
            },
        )


# Class-based views


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes a post by pk.
    View url: /posts/<pk>/delete/
    """

    model = Post
    template_name = "posts/confirm_delete.html"
    success_url = reverse_lazy("posts:main-post-view")

    def form_valid(self, *args, **kwargs):
        post = self.get_object()
        author = post.author
        author_email = author.user.email
        
        # If post's author user doesnt equal request's user or user is not staff.
        if (author.user != self.request.user) and not (self.request.user.is_staff):
            messages.add_message(
                self.request,
                messages.ERROR,
                "Vous n'êtes pas autorisé à supprimer ce post.",
            )
            return HttpResponseRedirect(self.success_url)

        # Executes only if post's author user
        # and request's user are the same
        # or if request's user is staff.
        self.object.delete()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Post supprimé avec succès !",
        )

        # Send a email if deletion by staff
        if self.request.user.is_staff:
            reason = self.request.POST.get("reason")

            message = render_to_string("posts/email_deleted_post.html", {
                'author': author,
                'post': post,
                'reason': reason,
            })

            with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
            ) as connection:
                subject = "Post deleted"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [
                    author_email,
                ]
                message = message
                EmailMessage(
                    subject, message, email_from, recipient_list, connection=connection
                ).send()

        return HttpResponseRedirect(self.success_url)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Updates a post by pk.
    View url: /posts/<pk>/update/
    (This view is (again) indentical to PostDeleteView)
    """

    model = Post
    form_class = PostCreateModelForm
    template_name = "posts/update.html"
    success_url = reverse_lazy("posts:main-post-view")

    def form_valid(self, form):
        profile = get_request_user_profile(self.request.user)

        if form.instance.author != profile:
            messages.add_message(
                self.request,
                messages.ERROR,
                "Vous n'êtes pas autorisé à modifier ce post.",
            )
            return HttpResponseRedirect(self.success_url)

        # Update the post
        self.object = form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Post mis à jour avec succès !",
        )
        return HttpResponseRedirect(self.success_url)
