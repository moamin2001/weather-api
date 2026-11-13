"""Fetch current weather from OpenWeatherMap and print a formatted summary."""

import os
import sys
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

API_URL = "https://api.openweathermap.org/data/2.5/weather"


@dataclass
class Weather:
    city: str
    country: str
    description: str
    temp_c: float
    feels_like_c: float
    humidity: int
    wind_speed: float

    @classmethod
    def from_api(cls, data: dict) -> "Weather":
        """Build a Weather object from the raw API JSON."""
        return cls(
            city=data["name"],
            country=data["sys"]["country"],
            description=data["weather"][0]["description"].capitalize(),
            temp_c=data["main"]["temp"],
            feels_like_c=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
        )

    def summary(self) -> str:
        lines = [
            f"Weather in {self.city}, {self.country}",
            "-" * 32,
            f"Conditions : {self.description}",
            f"Temperature: {self.temp_c:.1f} °C (feels like {self.feels_like_c:.1f} °C)",
            f"Humidity   : {self.humidity}%",
            f"Wind       : {self.wind_speed:.1f} m/s",
        ]
        return "\n".join(lines)


def fetch_weather(city: str, api_key: str) -> Weather:
    response = requests.get(
        API_URL,
        params={"q": city, "appid": api_key, "units": "metric"},
        timeout=10,
    )
    response.raise_for_status()
    return Weather.from_api(response.json())


def main() -> int:
    load_dotenv()  # reads .env in the current directory
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: OPENWEATHER_API_KEY is not set. Add it to your .env file.", file=sys.stderr)
        return 1

    city = sys.argv[1] if len(sys.argv) > 1 else "Cairo"

    try:
        weather = fetch_weather(city, api_key)
    except requests.HTTPError as exc:
        status = exc.response.status_code
        hint = {401: "invalid API key", 404: "city not found"}.get(status, "request failed")
        print(f"Error: {hint} (HTTP {status}).", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        return 1
    except (KeyError, IndexError, ValueError) as exc:
        print(f"Unexpected response format: {exc!r}", file=sys.stderr)
        return 1

    print(weather.summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
