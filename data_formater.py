from datetime import datetime


def openweather_format_weather_now(api_response: dict) -> dict:
    result = {
        "temperature": api_response["main"]["temp"],
        "feels_like": api_response["main"]["feels_like"],
        "date": datetime.fromtimestamp(api_response["dt"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "humidity": api_response["main"]["humidity"],
        "weather_type": api_response["weather"][0]["description"].capitalize(),
        "id": api_response["weather"][0]["id"],
    }
    return result


def openweather_format_forecast_by_days(api_response: dict) -> dict:
    result = {}
    for day_data in api_response["list"]:
        date = datetime.fromtimestamp(day_data["dt"]).strftime("%d.%m.%Y")
        if date not in result:
            result[date] = {
                "temperature": [],
                "feels_like": [],
                "humidity": [],
                "date": date,
                "weather_type": "",
                "id": 0,
            }
        result[date]["temperature"].append(day_data["main"]["temp"])
        result[date]["feels_like"].append(day_data["main"]["feels_like"])
        result[date]["humidity"].append(day_data["main"]["humidity"])
        result[date]["weather_type"] = day_data["weather"][0][
            "description"
        ].capitalize()
        result[date]["id"] = day_data["weather"][0]["id"]

    for date, weather in result.items():
        for weather_param_title, value in weather.items():
            if isinstance(value, list):
                weather[weather_param_title] = sum(value) / len(value)
        result[date] = weather

    return result


def openweather_format_forecast_by_hours(api_response: dict) -> dict:
    result = {}

    for hour_data in api_response["list"]:
        dt = datetime.fromtimestamp(hour_data["dt"])

        if dt.date() not in result:
            result[dt.date()] = {}

        result[dt.date()][dt.time()] = {
            "temperature": hour_data["main"]["temp"],
            "feels_like": hour_data["main"]["feels_like"],
            "humidity": hour_data["main"]["humidity"],
            "date": dt,
            "weather_type": hour_data["weather"][0]["description"].capitalize(),
            "id": hour_data["weather"][0]["id"],
        }
    return result