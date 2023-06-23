from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.quotes, name='home'),  # Головна сторінка, що відображає всі цитати
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  # Вам потрібно створити відповідний перегляд
    path('quotes/', views.quotes, name='quotes'),
    path('quotes/add/', views.add_quote, name='add_quote'),
    path('authors/<int:author_id>/', views.author, name='author'),
    path('tag/<slug:tag_slug>/page/<int:page>/', views.search_by_tag, name='quotes_by_tag'),
    path('scrape/', views.scrape_quotes, name='scrape_quotes'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # Ви можете додати інші шляхи тут, якщо потрібно
]
