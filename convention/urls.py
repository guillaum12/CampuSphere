from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import home_view, charte


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("allauth.urls")),
    path("", home_view, name="home-view"),
    path("charte/", charte, name="charte"),
    path("profiles/", include("profiles.urls")),
    path("posts/", include("posts.urls")),
    path("authentication/", include("authentication.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
