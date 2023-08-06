# Sunnyside

[![GitHub release](https://img.shields.io/github/v/release/junqili259/Sunnyside?include_prereleases)](https://github.com/junqili259/Sunnyside/releases)
![Python Version](https://img.shields.io/pypi/pyversions/sunnyside)

## Installation
```
pip3 install sunnyside
```

## Getting Started
### Python Version
Sunnyside only supports python 3.6+
_________________________________________________________________________________________________________________________________________________________________________________

```python
from sunnyside import Sunnyside

ref = Sunnyside("YOUR-API-KEY-HERE", "your-units-here") # Enter your api key here
```

## Current Weather
https://openweathermap.org/current

### Weather by city name
**Note**: Units are by default in Kelvin, to change units to imperial or celsius.

```python
weather = ref.current_weather()
response = weather.get_current_weather_by_city_name("city_name") # Enter your city name here
```
### Weather by city id
```python
response = weather.get_current_weather_by_city_id("city_id")
```
### Weather by coordinates 
```python
response = weather.get_current_weather_by_geo_coords("lat","lon")
```
### Weather by zip code
```python
response = weather.get_current_weather_by_zip_code("zipcode")
```

_________________________________________________________________________________________________________________________________________________________________________________
## 5 Day Weather Forecast
https://openweathermap.org/forecast5

### Weather by city name

```python
forecast = ref.five_day_forecast()
response = forecast.get_forecast_by_city_name("some_city_name_here")
```

### Weather by city id
```python
response = forecast.get_forecast_by_city_id("city_id")
```
### Weather by coordinates 
```python
response = forecast.get_forecast_by_geo_coords("lat","lon")
```
### Weather by zip code
```python
response = forecast.get_forecast_by_zip_code("zipcode")
```

_________________________________________________________________________________________________________________________________________________________________________________
## One Call
https://openweathermap.org/api/one-call-api


### Get weather data from one call api
```python
openweather = ref.one_call()
response = openweather.get_weather("33.441792","-94.037689")
```



_________________________________________________________________________________________________________________________________________________________________________________

## Reference
https://openweathermap.org/api

https://openweathermap.org/current

https://openweathermap.org/forecast5

https://openweathermap.org/api/one-call-api
