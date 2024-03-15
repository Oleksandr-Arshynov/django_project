
from django.urls import path
from . import views

from .views import AuthorDetailView

app_name = 'quotes'

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path('author/<str:fullname>/', AuthorDetailView.as_view(), name='author_detail'),
]