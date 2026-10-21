"""Data model for one saved weather reading."""
from datetime import datetime


class WeatherRecord:
    """A single weather observation for a city (encapsulates the data)."""

    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, city, country, temperature, humidity,
                 wind_speed, pressure, description, timestamp=None):
        self.city = city
        self.country = country
        self.temperature = float(temperature)   # °C
        self.humidity = float(humidity)         # %
        self.wind_speed = float(wind_speed)     # km/h
        self.pressure = float(pressure)         # hPa
        self.description = description
        self.timestamp = timestamp or datetime.now().strftime(self.TIME_FORMAT)

    def to_dict(self):
        """Convert to a plain dictionary (for JSON/CSV)."""
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, data):
        """Build a record from a dictionary loaded from file."""
        return cls(**data)

    def get_datetime(self):
        """Return the timestamp as a datetime object."""
        return datetime.strptime(self.timestamp, self.TIME_FORMAT)

    def __str__(self):
        return (f"[{self.timestamp}] {self.city}, {self.country}\n"
                f"  Temperature : {self.temperature:.1f} °C\n"
                f"  Humidity    : {self.humidity:.0f} %\n"
                f"  Wind speed  : {self.wind_speed:.1f} km/h\n"
                f"  Pressure    : {self.pressure:.0f} hPa\n"
                f"  Condition   : {self.description}")
