from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_of_day, name = 'newsToday'),
    path('archives/<int:year>/<int:month>/<int:day>/', views.past_days_news, name = 'pastNews'),
    path('search/', views.search_results, name = 'search_results')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)