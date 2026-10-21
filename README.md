# Weather Dashboard
### CS213 Python Course Project — Project #97

Weather Dashboard is a command-line application built using Python. It uses the Open-Meteo API to fetch current weather information for a city and saves the readings locally. Users can view previous records, calculate temperature statistics, generate charts, and export their weather history to a CSV file.

## Project Overview

Weather information is useful when planning trips, outdoor activities, and daily schedules. This project provides a simple way to check the current weather of a city and keep track of readings over time.

The application also allows users to view saved records, compare temperature and humidity values, and analyse weather data using charts.

## Objectives

- Fetch current weather information for a selected city.
- Display temperature, humidity, wind speed, pressure, and weather conditions.
- Save weather readings with date and time.
- View previously saved weather records for a city.
- Calculate maximum, minimum, and average temperature and average humidity.
- Generate line charts and bar charts using Matplotlib.
- Export saved records to a CSV file.
- Delete saved history for a selected city.
- Add sample data to test the application without an internet connection.

## Features

- **Current Weather:** Fetches weather information for a city using the Open-Meteo API.
- **Weather History:** Displays previously saved readings.
- **Temperature Summary:** Shows the highest, lowest, and average temperature, along with average humidity.
- **Line Chart:** Displays temperature and humidity trends across saved readings.
- **Bar Chart:** Compares temperatures from different readings.
- **CSV Export:** Saves weather records in CSV format for use in spreadsheet applications.
- **Delete History:** Removes saved records for a selected city after confirmation.
- **Demo Data:** Adds sample records for testing charts and other features offline.

## Technologies Used

- **Language:** Python 3
- **Weather API:** Open-Meteo
- **HTTP Requests:** Requests
- **Charts:** Matplotlib
- **Data Storage:** JSON
- **Data Export:** CSV
- **Code Editor:** Visual Studio Code
- **Version Control:** Git and GitHub

## Project Structure

```text
Weather_Dashboard/
│
├── main.py
├── api_client.py
├── models.py
├── storage.py
├── analytics.py
├── charts.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── history.json
│   └── weather_history.csv
│
└── charts/
    ├── city_line.png
    └── city_bar.png
```

The `data/` and `charts/` directories are created automatically when required. The generated files may not be present until the corresponding features are used.

### Main Python Files

| File | Purpose |
|---|---|
| `main.py` | Displays the menu and manages the program flow. |
| `api_client.py` | Handles city geocoding and weather API requests. |
| `models.py` | Defines the weather record model. |
| `storage.py` | Handles JSON storage and CSV export. |
| `analytics.py` | Calculates statistics from saved records. |
| `charts.py` | Generates and saves weather charts. |
| `config.py` | Stores API URLs, file paths, and weather-code descriptions. |

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip package installer
- Internet connection for live weather data

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Weather_Dashboard
```

Replace the placeholder with your GitHub repository URL.

### 2. Install the required packages

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
requests>=2.31.0
matplotlib>=3.8.0
```

### 3. Run the application

```bash
python main.py
```

## Application Menu

When the program starts, the following menu is displayed:

```text
1. Check current weather (and save it)
2. View saved history for a city
3. Show temperature summary
4. Line chart (temperature and humidity)
5. Bar chart (temperature)
6. Export CSV
7. Delete a city's history
8. Add demo data
0. Exit
```

Enter the number corresponding to the operation you want to perform.

## Data Source

This project uses the free [Open-Meteo API](https://open-meteo.com/) to retrieve weather information.

- **Geocoding API:** Finds the coordinates of a city.
- **Weather API:** Retrieves current weather measurements for those coordinates.

An API key is not required for standard use of these endpoints.

## Data Storage

Weather readings are stored locally in `data/history.json`. Each saved record contains the following information:

- City and country
- Latitude and longitude
- Temperature in degrees Celsius
- Relative humidity in percent
- Wind speed in kilometres per hour
- Surface pressure in hectopascals
- Weather description
- Date and time of the reading

The saved records can also be exported to `data/weather_history.csv`.

## Charts and Statistics

The application uses Matplotlib to generate two types of charts:

- **Line chart:** Shows temperature and humidity trends across saved readings.
- **Bar chart:** Compares the temperatures recorded at different times.

Generated charts are saved as PNG files in the `charts/` directory.

The statistics feature calculates the highest, lowest, and average temperature, as well as the average humidity, from the available records.

## Python Concepts Used

This project covers several Python concepts:

- Variables, data types, and operators
- Conditional statements and loops
- Functions and modular programming
- Lists and dictionaries
- Classes and object-oriented programming
- Dataclasses and encapsulation
- Exception handling
- File handling with JSON and CSV
- API requests
- Statistical calculations
- Data visualization using Matplotlib
- Modules, docstrings, and comments

## Testing

The following operations can be used to test the application:

1. Fetch weather information for a valid city and save the reading.
2. Enter an invalid city name and check how the application handles it.
3. View history when no records are available.
4. Generate temperature and humidity statistics.
5. Generate charts using saved readings.
6. Export the saved records to CSV.
7. Delete a city's history after confirmation.
8. Add demo data and test the features without an internet connection.

## Limitations

- Live weather data requires an internet connection.
- Weather information depends on the availability and response of the Open-Meteo API.
- Historical analysis is limited to readings saved by the application.
- Demo data is generated for testing and does not represent actual weather conditions.

## Future Improvements

The project can be extended with features such as:

- A graphical user interface
- Weather forecasts for upcoming days
- Date-range filters for saved records
- Additional statistics and charts
- Better handling of cities with similar names
- Automated unit tests

## Project Information

- **Course:** CS213 — Python
- **Project Number:** 97
- **Project Title:** Weather Dashboard
- **Language:** Python
