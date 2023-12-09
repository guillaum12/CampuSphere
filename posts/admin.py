from django.contrib import admin

from .models import Comment, Like, Post, Choice, Power

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Power)
admin.site.register(Choice)
