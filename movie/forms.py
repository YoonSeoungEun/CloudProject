from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')