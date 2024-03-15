from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from django.views.generic import DetailView

from .models import Author, Tag

from .utils import get_mongodb

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

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

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    slug_field = 'fullname'
    slug_url_kwarg = 'fullname'