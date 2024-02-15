import sqlite3
from sre_parse import CATEGORIES
from unicodedata import category
from zlib import MAX_WBITS
from django import forms
from .models import Choice, Post
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

class PostFilterForm(forms.Form):
    FILTER_CHOICES = [
        ('recent', 'Most recent'),
        ('favorite', 'Favorite'),
        ('votedpercentage', 'Best voted percentage'),
        ('many', 'Most rated'),
        #('reported', 'Most Reported'),
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
    
    new_posts = forms.BooleanField(required=False, label='New Posts')

class PostCreateModelForm(forms.ModelForm):
    title = forms.CharField(max_length=150, widget=forms.Textarea(attrs={"rows": 1}))
    content = forms.CharField(max_length=1000, widget=CKEditorWidget(), required=False)

    class Meta:
        model = Post
        fields = ("title", "content", "theme", "image")




class CommentCreateModelForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add a comment.."}),
        label="",
    )

    class Meta:
        model = Post
        fields = ("content",)

