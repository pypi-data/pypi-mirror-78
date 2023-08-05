from django.db import models
from django.db.models import Q

# Create your models here.
class subject(models.Model):
    name        = models.CharField(max_length=20,unique=True)
    last_num    = models.IntegerField(blank=False,null=False)	
    done_num    = models.IntegerField(blank=False,null=False)	
class lecture(models.Model):
    sub_name    = models.CharField(max_length=20)
    chapter     = models.CharField(max_length=5)
    screen      = models.BooleanField(blank=False,null=False)
    time        = models.BooleanField(blank=False,null=False)
    quiz        = models.BooleanField(blank=False,null=False)
    status      = models.IntegerField(default=1)	
class Post_test(models.Model):
    title    = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body     = models.TextField()
    class Meta:
        ordering =['-id']
class Post_test00(models.Model):
    title    = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body     = models.TextField()
    class Meta:
        db_table = 'music_ablbum'

from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
