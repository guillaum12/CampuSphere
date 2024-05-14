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
    hide_site_explanations,
    switch_like_comment,
    petitions,
)

app_name = "posts"

urlpatterns = [
    path("", show_first_posts, name="main-post-view"),
    path("petitions/", petitions, name="petitions-view"),
    path("<int:page_index>", show_selected_posts, name="following-post-view"),
    path("<pk>/show/", show_post, name="one-post-view"),
    path("never_display_explanations/", hide_site_explanations, name="never-display-explanations"),
    path("comment/", comment_view, name="comment-view"),
    path("like/", switch_like, name="switch-like-view"),
    path("like_comment/", switch_like_comment, name="switch-like-comment-view"),
    path("power/", power, name="switch-power-view"),
    path("feedback/", feedback, name="feedback-view"),
    path("report/", switch_report, name="switch-report-view"),
    path("<pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<pk>/update/", PostUpdateView.as_view(), name="post-update"),
]
