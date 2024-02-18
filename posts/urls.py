from django.urls import path

from .views import (
    PostDeleteView,
    PostUpdateView,
    show_first_posts,
    show_selected_posts,
    comment_view,
    switch_like,
    power,
    show_post, 
    switch_report,
    feedback,
)

app_name = "posts"

urlpatterns = [
    path("", show_first_posts, name="main-post-view"),
    path("<int:first_post_to_show>", show_selected_posts, name="following-post-view"),
    path("<pk>/show/", show_post, name="one-post-view"),
    path("comment/", comment_view, name="comment-view"),
    path("like/", switch_like, name="switch-like-view"),
    path("power/", power, name="switch-power-view"),
    path("feedback/", feedback, name="feedback-view"),
    path("report/", switch_report, name="switch-report-view"),
    path("<pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<pk>/update/", PostUpdateView.as_view(), name="post-update"),
]
