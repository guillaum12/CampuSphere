from django.contrib import admin

from .models import SwipeSurvey, SwipeQuestion, SwipePossibleAnswer, SwipeAnswerUser

# Register your models here.
admin.site.register(SwipeAnswerUser)
admin.site.register(SwipePossibleAnswer)
admin.site.register(SwipeQuestion)
admin.site.register(SwipeSurvey)
