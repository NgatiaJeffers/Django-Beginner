from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'article'),
    path("newToday/", views.news_today, name = "newsToday"),
    path('article/<int:article_id>/', views.article, name = 'article'),
    path('search/', views.search_results, name = 'search_results'),
    path('archives/<int:year>/<int:month>/<int:day>/', views.past_days_news, name = 'pastNews'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)