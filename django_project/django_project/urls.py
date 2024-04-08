
from django.contrib import admin
from django.urls import path, include

from users import views



urlpatterns = [
    path('auth/', include('users.urls')),
    path('', include('quotes.urls')),
    path('admin/', admin.site.urls),
]
