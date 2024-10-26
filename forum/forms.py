from django import forms
from django.forms import ModelForm
from forum.models import ForumQuestion, ForumReply

class NewForumForm(ModelForm):
    class Meta:
        model = ForumQuestion
        fields = ["title", "question", "topic"]

class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment...'})
        }