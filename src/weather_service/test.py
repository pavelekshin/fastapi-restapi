from src.weather_service.schemas import Weather

json = """{ "coord": {
    "lon": 37.6184,
    "lat": 55.7512
}, "base": "stations",
"main": {
    "temp": 18.58,
    "feels_like": 18.16,
    "temp_min": 17.15,
    "temp_max": 20.29,
    "pressure": 1027,
    "humidity": 64,
    "sea_level": 1027,
    "grnd_level": 1008
},
"visibility": 10000,
"wind": {
    "speed": 4.21,
    "deg": 65,
    "gust": 8.66
},
"rain": {
    "1h": 3.16
},
"clouds": {
    "all": 100
},
"dt": 1716744718,
"sys": {
    "type": 1,
    "id": 9029,
    "country": "RU",
    "sunrise": 1716685212,
    "sunset": 1716746000
},
"timezone": 10800,
"id": 524901,
"name": "Moscow",
"cod": 200
}"""

test2 = """
{
  "coord": {
    "lon": 37.6184,
    "lat": 55.7512
  },
  "base": "stations",
  "main": {
    "temp": 18.58,
    "feels_like": 18.16,
    "temp_min": 17.15,
    "temp_max": 20.29,
    "pressure": 1027,
    "humidity": 64,
    "sea_level": 1027,
    "grnd_level": 1008
  },
  "visibility": 10000,
  "wind": {
    "speed": 4.21,
    "deg": 65,
    "gust": 8.66
  },
  "clouds": {
    "all": 100
  },
  "rain": {
    "1h": 3.16,
    "3h": null
  },
  "snow": null,
  "dt": "2024-05-26T20:31:58+0300",
  "sys": {
    "type": 1,
    "id": 9029,
    "country": "RU",
    "sunrise": "2024-05-26T04:00:12+0300",
    "sunset": "2024-05-26T20:53:20+0300"
  },
  "timezone": "UTC+03:00",
  "id": 524901,
  "name": "Moscow",
  "cod": 200
}
"""

data = Weather.model_validate_json(json)
print(data)
print(data.model_dump())
print(data.model_dump_json(indent=2, context={}))
