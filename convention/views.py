from django.shortcuts import redirect, render
from posts.models import Post, Like
from django.contrib.auth.models import User


def home_view(request):
    """
    Welcoming page view, redirects to the board if user is authenticated.
    """
    if request.user.is_authenticated:
        return redirect("posts/")

    context = {
        "nombre_utilisateur": len(User.objects.all()),
        "nombre_post": len(Post.objects.all()),
        "nombre_like": len(Like.objects.all()),
    }

    return render(request, "main/home.html", context=context)


def charte(request):
    return render(request, "main/charte.html")
