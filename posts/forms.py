from django import forms

from .models import Post


class PostCreateModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={"rows": 1}))
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}))

    class Meta:
        model = Post
        fields = ("title", "content", "theme", "image")


class PostUpdateModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={"rows": 1}))
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}))

    class Meta:
        model = Post
        fields = ("title", "content", "theme")


class CommentCreateModelForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add a comment.."}),
        label="",
    )

    class Meta:
        model = Post
        fields = ("content",)
