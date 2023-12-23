from django.contrib import admin

from .models import Like, Post, Choice, Power

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Power)
admin.site.register(Choice)
