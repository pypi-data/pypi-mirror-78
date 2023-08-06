from .currentWeather import CurrentWeather
from .fiveDayForecast import FiveDayForecast
from .onecall import OneCall


class Sunnyside:
    def __init__(self, api_key, units= None):
        self.api_key = api_key
        self.units = units
    
    def current_weather(self):
        return CurrentWeather(self.api_key, self.units)

    def five_day_forecast(self):
        return FiveDayForecast(self.api_key, self.units)
    
    def one_call(self):
        return OneCall(self.api_key, self.units)