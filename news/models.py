from django.db import models

# Create your models here.
class Editor(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField()

    def __str__(self):
        return self.first_name

    def save_editor(self):
        self.save()
    class Meta:
        ordering = ['first_name']

class tags(models.Model):
    name = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length = 30)
    post = models.TextField()
    editor = models.ForeignKey(Editor, on_delete = models.CASCADE,)
    tags = models.ManyToManyField(tags)
    pub_date = models.DateTimeField(auto_now_add = True)
    article_image = models.ImageField(upload_to = 'articles/')

    @classmethod
    def days_news(cls, date):
        news = cls.objects.filter(pub_date_date = date)
        return news

    @classmethod
    def search_by_title(cls, search_term):
        news = cls.objects.filter(title__icontains = search_term)
        return news