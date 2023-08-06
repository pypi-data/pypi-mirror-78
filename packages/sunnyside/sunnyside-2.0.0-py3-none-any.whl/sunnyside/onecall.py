import requests

class OneCall():
    def __init__(self, api_key, units= None):
        self.api_key = api_key
        self.units = units

    def get_weather(self, lat, lon):

        if self.units is None:
            api_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={self.api_key}"
        else:
            api_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units={self.units}&appid={self.api_key}"

        response = requests.get(url= api_url)
        return response.json()