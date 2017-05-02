from app.controller.weather import Weather
from json import dumps
api = 'v3/location/search'
params = {'query' : 'Atlanta', 'locationType' : 'city', 'countryCode' : 'US', 'adminDistrictCode' : 'GA'}
weather = Weather(username='ad6fbabc-d710-4126-8764-3a12d5a85096', password='onPrMLvFGk', params=params, api_url=api)
print(dumps(weather.getWeather(), indent=2))

api = 'v1/geocode/45.42/75.69/forecast/daily/10day.json'
params = {'units' : 'm'}
weather = Weather(username='ad6fbabc-d710-4126-8764-3a12d5a85096', password='onPrMLvFGk', params=params, api_url=api)
print(dumps(weather.getWeather(), indent=2))