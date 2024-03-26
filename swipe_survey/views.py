from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SwipeSurvey

# Create your views here.


@login_required
def show_selected_swipe_survey(request, survey_index):
    survey = SwipeSurvey.objects.get(survey_id=survey_index)
    context = {
        "survey": survey
    }
    return render(request, "swipe_survey/main.html", context)
