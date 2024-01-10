from django.contrib import admin

from .models import Like, Post, Choice, Power, Report, Feedback

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Power)
admin.site.register(Report)
admin.site.register(Choice)

admin.site.register(Feedback)