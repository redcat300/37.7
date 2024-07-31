from django import forms
from .models import Ad, Response, Comment

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'content', 'category', 'image', 'video']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image', 'video']

class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image', 'video']

