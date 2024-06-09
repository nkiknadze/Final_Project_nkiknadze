from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/<str:city_name>/', views.delete_city, name='delete_city'),
    path('all_cities/', views.all_cities, name='all_cities'),
]