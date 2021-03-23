import datetime as dt
from .forms import NewsLetterForm
from .email import send_welcome_email
from .models import Article, NewsLetter
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
def news_of_day(request):
    date = dt.date.today()
    articles = Article.objects.all().order_by('-pub_date')
    
    return render(request, "all-news/today-news.html", {"date": date, "news": articles})

def past_days_news(request, past_date):

    try:
        # Converts  data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # Raise 422 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, "all-news/past-news.html", {"date": date, "news": news})

def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    if request.method == 'POST':
        form = NewsLetterForm(data=request.POST)
        if form.is_valid():
            print('valid')
            name = form.cleaned_date['name']
            email = form.cleaned_date['email']
            recipient = NewsLetter(name = name, email = email)
            recipient.save()
            send_welcome_email(name, email)

            HttpResponseRedirect('news_today')
        else:
            print('Error loading the data!')
    else:
        form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date": date, "news": news, "form": form})

def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html', {"message": message, "articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html', {"message": message})

def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ValueError:
        raise Http404()
    return render(request, "all-news/article.html", {"article": article})