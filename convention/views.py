import os
from django.conf import settings
from django.shortcuts import redirect, render
import pandas as pd
from posts.models import Post, Like
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
import matplotlib.pyplot as plt

def home_view(request):
    """
    Welcoming page view, redirects to the board if user is authenticated.
    """
    # if request.user.is_authenticated:
    #    return redirect("posts/")

    context = {
        "nombre_utilisateur": len(User.objects.all()),
        "nombre_post": len(Post.objects.all()),
        "nombre_like": len(Like.objects.all()),
    }

    return render(request, "main/home.html", context=context)


def charte(request):
    return render(request, "main/charte.html")

@staff_member_required
def statistics(request):
    
    user_signups = User.objects.values('date_joined')
    df = pd.DataFrame(user_signups)
    df['date_joined'] = pd.to_datetime(df['date_joined'])
    df.set_index('date_joined', inplace=True)
    cumulative_signups = df.resample('D').size().cumsum()
    plt.figure(figsize=(10, 6))
    cumulative_signups.plot()
    plt.title('Nombre cumulé d\'inscriptions au fil du temps')
    plt.xlabel('Date')
    plt.ylabel('Nombre cumulé d\'inscriptions')
    
    plt.tight_layout()
    
    path = os.path.join(settings.MEDIA_ROOT, 'graphs', 'cumulative_signup_graph.png')
    
    plt.savefig(path)  # Mettre le bon chemin
    plt.close()
    
    url = os.path.join(settings.MEDIA_URL, 'graphs', 'cumulative_signup_graph.png')
    
    context = {
        "url": url,
    }
    
    return render(request, "main/statistics.html", context=context)