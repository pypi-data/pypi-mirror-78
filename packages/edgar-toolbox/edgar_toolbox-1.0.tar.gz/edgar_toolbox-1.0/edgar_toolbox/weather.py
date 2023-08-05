# -*- coding: UTF-8 -*-

import sys
import requests

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

BASE_URI = "https://www.metaweather.com"

def search_city_code(query):
    city_url = f'{BASE_URI}/api/location/search/?query={query}'
    if requests.get(city_url).json():
        cities = requests.get(city_url).json()
        if len(cities) > 1:
            d_b = []
            for index, city in enumerate(cities):
                city_name = city['title']
                d_b.append({index:city_name})
            return multiple_city_filter(d_b)
        return cities[0]['woeid']
    return None

def multiple_city_filter(cities):
    d_b = {}
    for index, city in enumerate(cities):
        city_name = city[index]
        print(f'{index+1} {city_name}')
        stringed_index = str(index+1)
        d_b[stringed_index] = city_name
    choose = input('Which city did you mean?')
    query = d_b[choose]
    return search_city(query)

def weather_forecast(city):
    woeid = search_city_code(query)
    weather_url = f'{BASE_URI}/api/location/{woeid}'
    weather_forecast_json = requests.get(weather_url).json()

    return weather_forecast_json['consolidated_weather']

def main():
    query = input("City?\n> ")
    city = search_city(query)
    if isinstance(city, list):
        city = multiple_city_filter(city)
        print("Hey")
    woeid = city['woeid']
    print(city['title'])
    for weather in weather_forecast(woeid):
        date = weather['applicable_date']
        state = weather['weather_state_name']
        avg_temp = int(weather['the_temp'])
        forecast = f'{date}: {state} ({avg_temp}°C)'
        print(forecast)

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGood_bye!')
        sys.exit(0)
