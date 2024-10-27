from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ForumQuestion(models.Model):
    TOPIC_CHOICES = [
    ('Information', 'Information'),
    ('Foods', 'Foods'),
    ('Restaurants', 'Restaurants'),
    ('Recommendation', 'Reccomendation'),
    ('Experience', 'Experience'),
    ]
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    question = models.TextField()
    topic = models.CharField(max_length=25, choices=TOPIC_CHOICES, default='Information') 
    replycount = models.IntegerField(default=0)

class ForumReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(ForumQuestion, related_name='replies', on_delete=models.CASCADE)
    reply = models.TextField()

    def __str__(self):
        return f'Reply by {self.user.username} on {self.question.title}'