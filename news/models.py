import datetime as dt
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class tags(models.Model):
    name = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length = 30)
    post = models.TextField()
    editor = models.ForeignKey(User, on_delete = models.CASCADE,)
    tags = models.ManyToManyField(tags)
    pub_date = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to = 'articles/')

    @classmethod
    def todays_news(cls):
        today = dt.date.today()
        news = cls.objects.filter(pub_date__date = today)
        return news

    @classmethod
    def days_news(cls, date):
        news = cls.objects.filter(pub_date__date = date)
        return news

    @classmethod
    def search_by_title(cls, search_term):
        news = cls.objects.filter(title__icontains = search_term)
        return news

class NewsLetter(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()