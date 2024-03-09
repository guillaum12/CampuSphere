from time import time
from math import ceil
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
from posts.views_utils import get_theme_path_from_theme
from django.template.loader import render_to_string

from .forms import PostCreateModelForm, PostFilterForm
from .models import Post, Feedback, Choice
from .views_utils import (
    add_comment_if_submitted,
    add_post_if_submitted,
    get_post_id_and_post_obj,
    like_unlike_post,
    power_post,
    find_post_to_show,
    report_unreport_post,
    never_display_explanations,
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
def show_selected_posts(request, page_index):
    """
    Shows all posts considering the filters.
    View url: /posts/
    """
    # qs = Post.objects.get_related_posts(user=request.user)
    filter_form = PostFilterForm(request.GET)

    nb_post_per_page = 10

    post_to_show = find_post_to_show(
        request.user, filter_form,
    )
    nb_pages = ceil(len(post_to_show) / nb_post_per_page)
    if page_index >= nb_pages:
        page_index = 0
    post_to_show = post_to_show[page_index * nb_post_per_page: (page_index + 1) * nb_post_per_page]

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
            "Votre profil a été banni.",
        )

    # Récupération du thème actuel dans la requête get
    if Choice.objects.filter(theme_name=request.GET.get("themes")).exists():
        theme = Choice.objects.get(theme_name=request.GET.get("themes"))
        theme_path = get_theme_path_from_theme(request, theme)
    else:
        theme_path = []

    # Récupération des éventuels paramètres GET
    display_site_explanations = False
    if request.GET.get("display_site_explanations") == "True":
        display_site_explanations = True

    context = {
        "post_to_show": post_to_show,
        "profile": profile,
        "p_form": PostCreateModelForm(),
        "filter_form": filter_form,
        "nb_pages": nb_pages,
        "page_index": page_index,
        "next_page_index": min(page_index + 1, nb_pages - 1),
        "previous_page_index": max(page_index - 1, 0),
        "theme_path": theme_path,
        "display_site_explanations": display_site_explanations,
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
    # Arborescence des thèmes
    theme = Post.objects.get(pk=pk).theme
    theme_path = get_theme_path_from_theme(request, theme)

    # Valeur actuelle de la note donnée
    profile = get_request_user_profile(request.user)
    try:
        power = profile.power_set.get(post=Post.objects.get(pk=pk)).power
    except:
        power = -1

    context = {
        "post": Post.objects.get(pk=pk),
        "profile": get_request_user_profile(request.user),
        "theme_path": theme_path,
        "power": power,
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
        # Rendu du nouveau commentaire
        comment_html = add_comment_if_submitted(request, profile)
        # Rendu du toast de succès
        toast_html = render_to_string(
            "main/toast.html", {"id": 'success-new-comment-' + str(int(time() * 1e3 % 1e6)), "success": True, "message": "Commentaire posté avec succès ! Merci pour votre contribution."})

        if comment_html:
            return JsonResponse({'comment_html': comment_html, 'toast_html': toast_html})

    # En cas d'erreur
    toast_html = render_to_string(
        "main/toast.html", {"id": 'fail-new-comment' + str(int(time() * 1e3 % 1e6)), "success": False})
    return JsonResponse({"toast_html": toast_html})


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

        # Envoi d'un toast
        if report_added:
            message = "Signalement envoyé avec succès. L'équipe de modération va examiner le post."
        else:
            message = "Signalement retiré avec succès."
        toast_html = render_to_string(
            "main/toast.html", {"id": 'success-report-' + str(int(time() * 1e3 % 1e6)),
                                "success": True,
                                "message": message})

        # Return JSON response for AJAX script in report.js
        return JsonResponse(
            {
                "status": "success",
                "report_added": report_added,
                "report_number": post_obj.report_number,
                "toast_html": toast_html,
            },
        )
    # Préparation d'un toast
    toast_html = render_to_string(
        "main/toast.html", {"id": 'fail-report-' + str(int(time() * 1e3 % 1e6)), "success": False})
    report_added = False
    return JsonResponse({"toast_html": toast_html})


@login_required
def hide_site_explanations(request):
    """
    Never display site explanations again.
    View url: /posts/never_display_explanations/
    """
    if request.method == "POST":
        profile = get_request_user_profile(request.user)

        if never_display_explanations(profile):
            # Envoi d'un toast
            message = "Les explications ne seront plus affichées lors des prochaines connexions."
            toast_html = render_to_string(
                "main/toast.html", {"id": 'success-hide-site-explanations-' + str(int(time() * 1e3 % 1e6)),
                                    "success": True,
                                    "message": message})

            # Return JSON response for AJAX script in report.js
            return JsonResponse(
                {
                    "status": "success",
                    "toast_html": toast_html,
                },
            )
    # Préparation d'un toast
    toast_html = render_to_string(
        "main/toast.html", {"id": 'fail-hide-site-explanations-' + str(int(time() * 1e3 % 1e6)), "success": False})
    return JsonResponse({"toast_html": toast_html})


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

        # Création du toast
        if power_added:
            message = "Votre vote a bien été pris en compte !"
        else:
            message = "Votre vote a bien été retiré."

        toast_html = render_to_string(
            "main/toast.html", {"id": 'success-hide-site-explanations-' + str(int(time() * 1e3 % 1e6)),
                                "success": True,
                                "message": message})

        # Return JSON response for AJAX script in power.js
        return JsonResponse(
            {
                "post_progress": post_obj.progress,
                "voter_number": post_obj.voter_number,
                "power_added": power_added,
                "post_color": post_obj.get_color_progress,
                "toast_html": toast_html,
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
