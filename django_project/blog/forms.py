from django import forms

from .models import Comment


class CreateCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols': 80}), max_length=60, label='')

    class Meta:
        model = Comment
        fields = ['text']
        labels = False
        ordering = ['date_comment']
