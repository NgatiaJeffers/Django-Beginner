from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.news_of_day, name = 'newsToday'),
    path('dashboard/', views.dashboardView, name = "dashboard"),
    path('article/<int:article_id>/', views.article, name = 'article'),
    path('search/', views.search_results, name = 'search_results'),
    path('archives/<int:year>/<int:month>/<int:day>/', views.past_days_news, name = 'pastNews'),
    path('login/', LoginView.as_view(), name = "login_url"),
    path('register/', views.registerView, name = "register_url"),
    path('logout/', LogoutView.as_view(next_page = 'dashboard'), name = "logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)