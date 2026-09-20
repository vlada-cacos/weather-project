import requests
from rich import print
from rich.console import Console

# Supported API services names:
OPENWEATHER = "openweather"
console = Console()


def get_city():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    city = data["city"]
    return city


def get_coordinates():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    loc = data["loc"]
    latitude, longitude = loc.split(",")
    return float(latitude), float(longitude)


def get_weather_data_now(api_service_name: str) -> dict:
    latitude, longitude = get_coordinates()
    if api_service_name == OPENWEATHER:
        with console.status("[bold blue]Получаем погодные данные...", spinner="earth"):
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather?",
                params={
                    "lat": latitude,
                    "lon": longitude,
                    "appid": "4b741c1b8c51fc0d81e1a75a82b8f58d",
                    "units": "metric",
                    "lang": "ru",
                },
            ).json()
        return response
    else:
        return {"message": "unexpected api service"}


def get_weather_data_forecast(api_service_name: str) -> dict:
    latitude, longitude = get_coordinates()
    if api_service_name == OPENWEATHER:
        with console.status(
            "[bold blue]Получаем погодные данные...", spinner="weather"
        ):
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={
                    "lat": latitude,
                    "lon": longitude,
                    "appid": "4b741c1b8c51fc0d81e1a75a82b8f58d",
                    "units": "metric",
                    "lang": "ru",
                },
            ).json()
        return response
    else:
        return {"message": "unexpected api service"}