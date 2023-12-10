from django.urls import path

from .views import (
    CommentDeleteView,
    PostDeleteView,
    PostUpdateView,
    post_comment_create_and_list_view,
    switch_like,
    power,
    favorite_post,
    show_post
)

app_name = "posts"

urlpatterns = [
    path("", post_comment_create_and_list_view, name="main-post-view"),
    path("favorite/", favorite_post, name="favorite-post-view"),
    path("<pk>/show/", show_post, name="one-post-view"),
    path("like/", switch_like, name="switch-like-view"),
    path("power/", power, name="switch-power-view"),
    path("<pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("comments/<pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
]
