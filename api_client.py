"""Talks to the Open-Meteo API: city name -> coordinates -> current weather."""
import requests

import config
from models import WeatherRecord


class WeatherAPIError(Exception):
    """Raised when weather data cannot be fetched."""


def _get_json(url, params):
    """GET a URL and return JSON, converting network problems to WeatherAPIError."""
    try:
        response = requests.get(url, params=params, timeout=config.REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise WeatherAPIError("No internet connection.")
    except requests.exceptions.Timeout:
        raise WeatherAPIError("The request timed out. Try again.")
    except requests.exceptions.HTTPError as err:
        raise WeatherAPIError(f"Server error: {err}")
    except ValueError:
        raise WeatherAPIError("Received invalid data from the server.")


def find_city(name):
    """Return (city, country, latitude, longitude) for a city name."""
    data = _get_json(config.GEOCODE_URL, {"name": name, "count": 1})
    results = data.get("results")
    if not results:
        raise WeatherAPIError(f"City '{name}' not found.")
    top = results[0]
    return top["name"], top.get("country", "N/A"), top["latitude"], top["longitude"]


def fetch_current_weather(city_name):
    """Fetch current weather for a city and return a WeatherRecord."""
    city, country, lat, lon = find_city(city_name)
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,"
                   "surface_pressure,weather_code",
    }
    current = _get_json(config.FORECAST_URL, params).get("current")
    if not current:
        raise WeatherAPIError("Weather data missing in response.")
    code = current.get("weather_code")
    return WeatherRecord(
        city=city,
        country=country,
        temperature=current["temperature_2m"],
        humidity=current["relative_humidity_2m"],
        wind_speed=current["wind_speed_10m"],
        pressure=current["surface_pressure"],
        description=config.WEATHER_CODES.get(code, f"Code {code}"),
    )
