import sqlite3
from django import forms

from profiles.views_utils import get_request_user_profile
from .models import Choice, Post
from ckeditor.widgets import CKEditorWidget

class PostFilterForm(forms.Form):
    FILTER_CHOICES = [
        ('--', 'Les plus pertinents'),
        ('recent', 'Les plus récents'),
        ('favorite', 'Mes favoris'),
        ('votedpercentage', 'Meilleures notes'),
        ('many', 'Les plus notés'),
        # ('reported', 'Most Reported'),
    ]

    filter_option = forms.ChoiceField(choices=FILTER_CHOICES, required=False)
    try:
        THEMES = Choice.objects.all().values_list('theme_name', 'theme_name')
        THEMES = list(THEMES)
        THEMES.append(('-', '---------'))
        THEMES.reverse()
        themes = forms.ChoiceField(choices=THEMES, required=False)

    except sqlite3.OperationalError:
        print('Table Choice does not exist')

    campus = forms.ChoiceField(choices=Post.CAMPUS_CHOICES, required=False, initial='--')
    new_posts = forms.BooleanField(required=False, label='New Posts')
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        profile = get_request_user_profile(user)
        associations_choices = [(0, "--")] + [(a.id, a.name) for a in profile.assos.all()]
        
        self.fields['associations'] = forms.ChoiceField(choices=associations_choices, required=False)

class PostCreateModelForm(forms.ModelForm):
    title = forms.CharField(max_length=150, widget=forms.Textarea(attrs={"rows": 1}))
    content = forms.CharField(max_length=1000, widget=CKEditorWidget(), required=False)

    class Meta:
        model = Post
        fields = ("title", "content", "campus", "theme", "image")


class CommentCreateModelForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add a comment.."}),
        label="",
    )

    class Meta:
        model = Post
        fields = ("content",)
