import argparse
from view import print_weather_now, print_weather_forecast


def parse_args():
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--high-precision",
        action="store_true",
        required=False,
        help="Highly accurate data",
    )
    common_parser.add_argument(
        "--full-info", action="store_true", required=False, help="Print with JSON"
    )

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparser_now = subparsers.add_parser("now", parents=[common_parser])
    subparser_forecast = subparsers.add_parser("forecast", parents=[common_parser])

    subparser_forecast.add_argument(
        "--with-time",
        action="store_true",
        required=False,
        help="Give an hourly weather forecast",
    )
    subparser_forecast.add_argument(
        "-d", "--days", type=int, choices=[1, 2, 3, 4], default=4, help="Number of days"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "now":
        print_weather_now(high_precision=args.high_precision, full_info=args.full_info)
    elif args.command == "forecast":
        print_weather_forecast(
            with_time=args.with_time,
            days=args.days,
            high_precision=args.high_precision,
            full_info=args.full_info,
        )


if __name__ == "__main__":
    main()