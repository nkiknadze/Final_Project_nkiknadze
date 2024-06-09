from django.shortcuts import render, redirect
import requests
from django.urls import reverse
from .models import City
from .forms import CityForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

def index(request):
    appid = '200af4996e6aa897eb6470dae573a038'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=Metric&appid=' + appid
    
    error_message = ''
    added_successfully = False

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            new_city_lower = new_city.lower()
            if not City.objects.filter(name__iexact=new_city_lower).exists():
                res = requests.get(url.format(new_city)).json()
                try:
                    temperature = res["main"]["temp"]
                    country = res["sys"]["country"]
                    weather_icon = res["weather"][0]["icon"]
                    user = request.user
                    City.objects.create(name=new_city, temperature=temperature, country=country, weather_icon=weather_icon, user=user)
                    added_successfully = True
                except KeyError:
                    error_message = f"Data for {new_city} is incomplete or missing."
            else:
                error_message = 'City is already in the database!'
        else:
            error_message = 'Invalid form data!'
            form = CityForm()
    else:
        form = CityForm()

    cities = City.objects.all().order_by('-id')[:3]
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        try:
            temperature = res["main"]["temp"]
            country = res["sys"]["country"]
            weather_icon = res["weather"][0]["icon"]
            city.temperature = temperature
            city.country = country
            city.weather_icon = weather_icon
            city.save()
        except KeyError:
            error_message = f"Data for {city.name} is incomplete or missing."

    all_cities = []
    for city in cities:
        city_info = {
            'city': city.name,
            'success': True,
            'temp': city.temperature,
            'icon': city.weather_icon,
            'country': city.country,
            'user': city.user
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities,
               'form': form, 
               'error_message': error_message, 
               'added_successfully': added_successfully}
    
    return render(request, 'weather/index.html', context)

@login_required
def delete_city(request, city_name):
    city = City.objects.filter(name__iexact=city_name, user=request.user)
    if city.exists():
        city.delete()
    return redirect(reverse('index'))

def all_cities(request):
    cities = City.objects.all()
    context = {'cities': cities}
    return render(request, 'weather/all_cities.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'weather/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'weather/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))
