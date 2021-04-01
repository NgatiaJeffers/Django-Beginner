import datetime as dt

from django.http.response import JsonResponse
from .forms import NewsLetterForm, NewArticleForm
from .email import send_welcome_email
from .models import Article, NewsLetter
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

# Create your views here.
def index(request):
    articles = Article.objects.all().order_by("-published")

    context = {
        "articles": articles
    }
    return render(request, 'index.html', context)

@login_required
def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    form = NewsLetter()
    if request.method == 'POST':
        form = NewsLetterForm(data=request.POST)
        if form.is_valid():
            print('valid')
            name = form.cleaned_date['your_name']
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

@login_required
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

@login_required
def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html', {"message": message, "articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html', {"message": message})

@login_required(login_url='accounts/login/')
def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ValueError:
        raise Http404()
    return render(request, "all-news/article.html", {"article": article})

@login_required(login_url="/accounts/login/")
def new_article(request):
    current_user = request.user
    if request.method == "POST":
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit = False)
            article.editor = current_user
            
            article.save()
        return redirect("NewsToday")

    else:
        form = NewArticleForm()
    return render(request, "all-news/new_article.html", {"form": form})

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetter(name = name, email = email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully aded to mailing list'}
    return JsonResponse(data)