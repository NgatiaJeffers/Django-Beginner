from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_of_day, name = 'newsToday'),
    path('archives/<int:year>/<int:month>/<int:day>/', views.past_days_news, name = 'pastNews')
]