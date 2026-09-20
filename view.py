from datetime import datetime
import api
import data_formater
from utils import round_json
from rich import print
from rich.panel import Panel, Panel
from rich.console import Console
from rich.text import Text
from rich.table import Table

console = Console()


def print_weather_now(high_precision=False, full_info=False) -> None:
    api_response = api.get_weather_data_now(api.OPENWEATHER)
    format_responce = data_formater.openweather_format_weather_now(api_response)

    if not high_precision:
        format_responce = round_json(format_responce)

    if full_info:
        print(api_response)
        return

    date_str = Text("Дата:", style="bold blue")
    date_int = Text(str(format_responce["date"]), style="bold blue")
    temp_str = Text("Температура:", style="bold dark_sea_green4")
    temp_int = Text(str(format_responce["temperature"]), style="medium_turquoise")
    feels_like_str = Text("Ощущается как:", style="bold dark_sea_green4")
    feels_like_int = Text(str(format_responce["feels_like"]), style="medium_turquoise")
    humidity_str = Text("Влажность:", style="bold dark_sea_green4")
    humidity_int = Text(str(format_responce["humidity"]), style="medium_turquoise")
    type_weather = Text(
        str(format_responce["weather_type"]), style="bold dark_sea_green4"
    )

    content_parts = [
        Text.assemble(date_str, date_int),
        Text(""),
        Text.assemble(temp_str, temp_int),
        Text.assemble(feels_like_str, feels_like_int),
        Text.assemble(humidity_str, humidity_int),
        Text.assemble(type_weather),
    ]
    content = Text("\n").join(content_parts)

    panel = Panel(
        content,
        title=f"[bold]🌤️ {api.get_city()} 🌤️",
        border_style="bold medium_turquoise",
        width=40,
        padding=(1, 5),
    )
    console.print(panel)


def print_weather_forecast(
    with_time=False, days=1, high_precision=False, full_info=False
) -> None:
    api_response = api.get_weather_data_forecast(api.OPENWEATHER)

    if not high_precision:
        api_response = round_json(api_response)

    if full_info:
        print(api_response)
        return

    print(f"Погода в {api.get_city()}:")
    if with_time:
        _print_forecast_with_time(
            filter_hourly_forecast(
                data_formater.openweather_format_forecast_by_hours(api_response), days
            )
        )
    else:
        _print_forecast_by_days(
            data_formater.openweather_format_forecast_by_days(api_response),
            high_precision,
            days,
        )


def filter_hourly_forecast(forecast_data: dict, days: int) -> dict:
    filtered_forecasts = {}
    unique_dates = set()

    for date, hourly_forecast in forecast_data.items():
        if date == datetime.now().date():
            filtred_hourly_forecast = {}
            for time, weather in hourly_forecast.items():
                if time >= datetime.now().time():
                    filtred_hourly_forecast[time] = weather
            hourly_forecast = filtred_hourly_forecast

        if len(unique_dates) >= days:
            break

        unique_dates.add(date)

        filtered_forecasts[date] = hourly_forecast

    return filtered_forecasts


def _print_forecast_with_time(weather_hourly_forecast: dict) -> None:
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("Дата:", style="dim", width=12)
    table.add_column("Время:")
    table.add_column("Температура:")
    table.add_column("Ощущается как:")
    table.add_column("Влажность:")
    table.add_column("Тип:")

    for date, horly_forecast in weather_hourly_forecast.items():
        d = str(date)
        for time, weather in horly_forecast.items():
            table.add_row(
                d,
                str(time),
                str(weather["temperature"]),
                str(weather["feels_like"]),
                str(weather["humidity"]),
                str(weather["weather_type"]),
            )
            d = ""

    console.print(table)


def _print_forecast_by_days(
    weather_daily_forecast: dict, high_precision: bool, days: int
) -> None:
    count = 0
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("Дата:", style="dim", width=12)
    table.add_column("Температура:")
    table.add_column("Ощущается как:")
    table.add_column("Влажность:")
    table.add_column("Тип:")

    for date, weather in weather_daily_forecast.items():
        if count >= days:
            break

        if not high_precision:
            my_round = round
        else:
            my_round = lambda x: x

        table.add_row(
            str(date),
            str(my_round(weather["temperature"])),
            str(my_round(weather["feels_like"])),
            str(my_round(weather["humidity"])),
            str(weather["weather_type"]),
        )
        count += 1
    console.print(table)