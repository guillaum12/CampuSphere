from django.urls import path

from .views import (show_selected_swipe_survey)

app_name = "swipe_survey"

urlpatterns = [
    path("<int:survey_index>", show_selected_swipe_survey, name="following-post-view"),
]
