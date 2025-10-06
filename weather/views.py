from django.shortcuts import render
from django.conf import settings
import requests

# Always get the API key from settings
API_KEY = settings.OPENWEATHER_API_KEY


def index(request):
    return render(request, 'weather/index.html')


def result(request):
    if request.method == 'POST':
        city_input = request.POST.get('city', '').strip()
        if not city_input:
            return render(request, 'weather/index.html', {'error': 'Please enter a city name.'})

        city = city_input.title()  # Capitalize properly

        # Current weather API
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            current_response = requests.get(current_url).json()
        except requests.exceptions.RequestException:
            return render(request, 'weather/index.html', {'error': 'Unable to connect to weather service.'})

        if current_response.get('cod') != 200:
            error_message = current_response.get('message', 'City not found')
            return render(request, 'weather/index.html', {'error': f"Error: {error_message.capitalize()}"})

        current_weather = {
            'city': city,
            'temperature': current_response['main']['temp'],
            'humidity': current_response['main']['humidity'],
            'description': current_response['weather'][0]['description'].capitalize(),
            'icon': current_response['weather'][0]['icon'],
        }

        # Clothing suggestion
        temp = current_weather['temperature']
        if temp > 30:
            current_weather['suggestion'] = "Wear light clothes"
        elif temp > 20:
            current_weather['suggestion'] = "T-shirt and jeans are fine"
        elif temp > 10:
            current_weather['suggestion'] = "Wear a jacket"
        else:
            current_weather['suggestion'] = "Wear heavy winter clothes"

        # 5-day forecast API
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        try:
            forecast_response = requests.get(forecast_url).json()
        except requests.exceptions.RequestException:
            return render(request, 'weather/index.html', {'error': 'Unable to fetch forecast data.'})

        if forecast_response.get('cod') not in ['200', 200]:
            error_message = forecast_response.get('message', 'Forecast data not found')
            return render(request, 'weather/index.html', {'error': f"Error: {error_message.capitalize()}"})

        # Prepare forecast data (pick one data point per day)
        forecast_list = []
        labels = []  # for Chart.js
        temps = []   # for Chart.js

        for i in range(0, len(forecast_response['list']), 8):  # Every 8 steps ≈ 1 day
            data = forecast_response['list'][i]
            day_forecast = {
                'date': data['dt_txt'].split(' ')[0],
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
            }
            forecast_list.append(day_forecast)
            labels.append(day_forecast['date'])
            temps.append(day_forecast['temp'])

        context = {
            'current_weather': current_weather,
            'forecast_list': forecast_list,
            'labels': labels,
            'temps': temps,
        }

        return render(request, 'weather/result.html', context)

    # If not POST, just render index
    return render(request, 'weather/index.html')
