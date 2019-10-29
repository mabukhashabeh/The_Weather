from django.shortcuts import render, HttpResponse
import requests
from weather.forms import CityForm
import json


def home(request):
    context = {}
    city = 'amman'
    form = CityForm(request.POST or None)
    if request.is_ajax():
        name = request.GET.get('city', 'amman')
        cities = prepare_cities_json_file(name)
        results = []
        for c in cities:
            results.append(c)
        data = json.dumps(results[:5])
        return HttpResponse(data, 'application/json')

    if request.method == "POST" and form.is_valid():
        city = request.POST.get('name')

    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=7da69195ddef314b85013d40d9b594ee&units=metric".format(
        city)
    response = requests.get(url).json()

    city_details = {}
    if response['cod'] == 200:
        city_details = {
            'not_found': False,
            'name': city,
            'description': response['weather'][0]['description'],
            'temp': response['main']['temp'],
            'icon': response['weather'][0]['icon'],
        }
    else:
        city_details['not_found'] = True

    context['city'] = city_details
    context['form'] = form
    return render(request, 'weather/weather.html', context)


def prepare_cities_json_file(prefix):
    json_file = json.loads(open('weather/city.list.json').read())
    cities = []
    for data in json_file:
        if data['name'].lower().startswith(prefix):
            cities.append(data['name'])
    return cities
