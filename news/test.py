from django.test import TestCase
from .models import Editor, Article, Tags
import datetime as dt

# Create your tests here.
class EditorTestCase(TestCase):

    # Set up method
    def setUp(self):
        self.dev = Editor(first_name = 'Dev', last_name = 'Gakuya', email = 'devgakuya@gmail.com')

    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.dev, Editor))

    # Testing Save Method
    def test_save_method(self):
        self.dev.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)

class ArticleTestCase(TestCase):

    def setUp(self):
        # Creating a new editor snd saving it
        self.dev = Editor(first_name = 'Dev', last_name = 'Gakuya', email = 'devgakuya@gmail.com')
        self.dev.save_editor()

        # Creating a new tag
        self.new_tag = Tags(name = 'testing')
        self.new_tag.save()

        # Creatitng a new article
        self.new_article = Article(title = 'Tech World', post = 'Talk is cheap show me the code', editor = self.dev)
        self.new_article.save()

        self.new_article.Tags.add(self.new_tag)

        # Deleting all instances
        def tearDown(self):
            Editor.objects.all().delete()
            Tags.objects.all().delete()
            Article.objects.all().delete()

        # Creating a test for the days article
        def test_get_news_today(self):
            today_news = Article.todays_news()
            self.assertTrue(len(today_news) > 0)

        # Geting the days date
        def test_get_news_by_date(self):
            test_date = '2021-03-16'
            date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
            news_by_date = Article.days_news(date)
            self.asserTrue(len(news_by_date) == 0)