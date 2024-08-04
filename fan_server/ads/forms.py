from django import forms
from .models import Ad, Response, Comment
from ckeditor.widgets import CKEditorWidget
from django import forms


class AdForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Ad
        fields = ['title', 'content', 'category']


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

