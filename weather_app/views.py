from django.http import HttpResponseRedirect
from django.shortcuts import render
from ipware import get_client_ip
from .utils import ipInfo, infoWeather
from .models import City
from .forms import CityForm
from django import template


def getlocation(request):
    client_ip, is_routable = get_client_ip(request)
    return client_ip, is_routable


register = template.Library()


# @register.simple_tag
# def delete_city(city_now, city):
#     City.objects.filter(city=city).delete()
#     return HttpResponseRedirect(f'/{city_now}/')


def index(request, city=''):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(f'/{form.data["city"]}/')
    else:
        form = CityForm()
        client_ip, is_routable = getlocation(request)
        cities = City.objects.all().order_by('-id')
        if city:
            context = {'city': city}
            if not City.objects.all().filter(city=city):
                c = City(city=city)
                c.save()
            else:
                City.objects.filter(city=city).delete()
                c = City(city=city)
                c.save()
        else:
            if client_ip == '127.0.0.1':
                context = {'city': 'Tomsk'}
            else:
                context = {'city': ipInfo(client_ip)}
        context['cities'] = cities
        context['now'], context['forecast'] = infoWeather(context['city'])
        try:
            if len(context['now'][0].split()) > 2:
                context['check_weather_now'] = context['now'][0].split()[2].lower()
            else:
                context['check_weather_now'] = context['now'][0].split()[1].lower()
        except Exception:
            try:
                context['check_weather_now'] = context['now'][0]
            except Exception:
                pass
            pass
        if context['now'] and context['forecast']:
            return render(request, 'weather_app/index.html', {'context': context, 'form': form})
        else:
            City.objects.filter(city=context['city']).delete()
            context['city'] = ''
            return render(request, 'weather_app/index.html', {'context': context, 'form': form})


def about(request):
    return render(request, 'weather_app/about.html')
