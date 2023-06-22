# views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Author, Quote, Tag
from django.db.models import Count
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'StarkApp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def quotes(request):
    quotes = Quote.objects.all()
    return render(request, 'StarkApp/quotes.html', {'quotes': quotes})


@login_required
def add_quote(request):
    if request.method == 'POST':
        quote_text = request.POST.get('quote')
        author_name = request.POST.get('author')
        author, _ = Author.objects.get_or_create(name=author_name)
        quote = Quote.objects.create(quote=quote_text, author=author, user=request.user)
        return redirect('quotes')
    else:
        return render(request, 'StarkApp/add_quote.html')


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'StarkApp/author.html', {'author': author})


def logout(request):
    auth_logout(request)
    return redirect('home')  # redirect to homepage after logging out


def search_by_tag(request, tag_slug, page=1):
    quotes_list = Quote.objects.filter(tags__name=tag_slug)  # заменил `tags__slug` на `tags__name`
    paginator = Paginator(quotes_list, 10)  # показывать 10 цитат на странице

    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, вывести первую страницу.
        quotes = paginator.page(1)
    except EmptyPage:
        # Если страница вне диапазона (например, 9999), вывести последнюю страницу результатов.
        quotes = paginator.page(paginator.num_pages)

    return render(request, 'StarkApp/search_results.html', {'quotes': quotes})


def top_ten_tags(request):
    tags = Tag.objects.annotate(total=Count('quote')).order_by('-total')[:10]
    return render(request, 'StarkApp/top_tags.html', {'tags': tags})


def scrape_quotes(request):
    response = requests.get('https://yourwebsite.com/quotes')
    soup = BeautifulSoup(response.text, 'html.parser')

    for quote_element in soup.find_all('div', class_='quote'):
        quote_text = quote_element.find('span', class_='text').get_text()
        quote, created = Quote.objects.get_or_create(quote=quote_text)  # Используйте quote вместо text
        # ... more code to handle tags, etc ...
        print(f'Створена цитата: {quote_text}')  # Вывести цитату в консоль

    return HttpResponse('Scraping Done!')
