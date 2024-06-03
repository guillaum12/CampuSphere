from django.contrib import admin

from .models import Like, Post, Choice, Power, Report, Feedback

admin.site.register(Like)
admin.site.register(Power)
admin.site.register(Report)
admin.site.register(Choice)

admin.site.register(Feedback)


class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_post', 'is_troll', 'theme')
    list_filter = ('is_post', 'is_troll', 'theme')
    actions = ['make_troll']

    def make_troll(self, request, queryset):
        queryset.update(status='is_troll')
    make_troll.short_description = 'Marquer comme troll'

admin.site.register(Post, PostAdmin)