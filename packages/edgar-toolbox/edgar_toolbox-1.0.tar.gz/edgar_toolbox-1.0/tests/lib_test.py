# -*- coding: UTF-8 -*-

# Import from standard library
import os
import edgar_toolbox
import pandas as pd
# Import from our lib
from edgar_toolbox.lib import weather_forecast, search_city_code
import pytest

def test_weather_forecast():
    assert weather_forecast('Paris').shape == (6,15)

def test_search_city_code():
    assert search_city_code('Paris') == 615702
    assert search_city_code('London') == 44418
