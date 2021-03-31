import datetime as dt
from .forms import NewsLetterForm, ArticleForm
from .email import send_welcome_email
from .models import Article, NewsLetter
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def index(request):
    articles = Article.objects.all().order_by("-pub_date")

    context = {
        "articles": articles
    }
    return render(request, 'index.html', context)

@login_required
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

            return redirect('news_today')
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

@login_required
def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ValueError:
        raise Http404()
    return render(request, "all-news/article.html", {"article": article})

@login_required
@csrf_protect
def add_article(request):
    form = ArticleForm(request.POST, request.FILES)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            post = Article(
                image = form.cleaned_data["image"],
                title = form.cleaned_data["title"],
                post = form.cleaned_data["new_article"],
                editor = request.user
            )

            post.save()
            print(post)

            post_name = form.cleaned_data.get("title")
            messages.success(request, f'Post created {post_name} !')
            return redirect("home")

    else:
        form = ArticleForm()

    return render(request, "all-news/article.html", {"form": form})
