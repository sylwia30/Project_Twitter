from django import forms

from .models import Comment


class CreateCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols': 80}), label='')
    class Meta:
        model = Comment
        fields = ['text']
        labels = False