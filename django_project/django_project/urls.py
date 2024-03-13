
from django.contrib import admin
from django.urls import path, include

from users import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('', include('quotes.urls')),
    path('register/', views.register, name='register'), 
    path('login/', views.login, name='login'), 
    path('logout/', views.logout, name='logout'),
]
