from django.urls import path

from .views import (
    CommentDeleteView,
    PostDeleteView,
    PostUpdateView,
    post_comment_create_and_list_view,
    switch_like,
    power,
    favorite_post,
    show_post, 
    report,
    switch_report
)

app_name = "posts"

urlpatterns = [
    path("<str:sort>/", post_comment_create_and_list_view, name="main-post-view"),
    path("favorite/", favorite_post, name="favorite-post-view"),
    path("<pk>/show/", show_post, name="one-post-view"),
    path("like/", switch_like, name="switch-like-view"),
    path("power/", power, name="switch-power-view"),
    path("report/", switch_report, name="switch-report-view"),
    path("<pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("<pk>/update/", report, name="post-report"),
    path("comments/<pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
]
