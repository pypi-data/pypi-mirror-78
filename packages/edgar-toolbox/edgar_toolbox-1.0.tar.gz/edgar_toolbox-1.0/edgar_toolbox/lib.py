# -*- coding: UTF-8 -*-

from os.path import split
import pandas as pd
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
    woeid = search_city_code(city)
    weather_url = f'{BASE_URI}/api/location/{woeid}'
    weather_forecast_json = requests.get(weather_url).json()
    return pd.DataFrame(weather_forecast_json['consolidated_weather'])

if __name__ == "__main__":
    # For introspections purpose to quickly get this functions on ipython
    import edgar_toolbox
    data = weather_forecast('Paris')
    data =pd.DataFrame(data)
    data_bis = search_city_code('London')
    print(data.shape)
    print(data_bis)
