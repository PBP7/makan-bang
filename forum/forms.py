from django import forms
from django.forms import ModelForm
from forum.models import ForumQuestion, ForumReply
from django.utils.html import strip_tags

class NewForumForm(ModelForm):
    class Meta:
        model = ForumQuestion
        fields = ["title", "question", "topic"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        return strip_tags(title)
    
    def clean_question(self):
        question = self.cleaned_data["question"]
        return strip_tags(question)


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment...'})
        }
    
    def clean_reply(self):
        reply = self.cleaned_data["reply"]
        return strip_tags(reply)