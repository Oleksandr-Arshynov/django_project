from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import AuthorForm, QuoteForm
from django.shortcuts import render
from django.http import HttpResponse
from scrapy.crawler import CrawlerProcess
from .import_quotes import QuotesSpider
from .models import Author, Quote, Tag

from .utils import get_mongodb


from django.contrib import messages
from django.core.mail import send_mail


def main(request, page=1):
    per_page = 10
    quotes = Quote.objects.all().select_related('author')
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.get_page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:root')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:root')
    else:
        form = QuoteForm()
    authors = Author.objects.all()
    tags = Tag.objects.all() 
    return render(request, 'quotes/add_quote.html', {'form': form, 'authors': authors, 'tags':tags})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})

def quotes_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes_with_tag = Quote.objects.filter(tags=tag)
    return render(request, 'quotes/quotes_by_tag.html', {'tag': tag, 'quotes_with_tag': quotes_with_tag})





@login_required
def run_scraping(request):
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
    return HttpResponse("Scraping process initiated successfully.")
