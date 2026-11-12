
import requests

def get_weather(city):

    # Find the city coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(geo_url, params=geo_params, timeout=15)
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    if "results" not in geo_data:
        print("City not found. Please try another city.")
        return

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]
    country = location.get("country", "Unknown")

    # Get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,"
                   "apparent_temperature,weather_code,wind_speed_10m",
        "timezone": "auto"
    }

    response = requests.get(
        weather_url, params=weather_params, timeout=15
    )
    response.raise_for_status()

    data = response.json()
    current = data["current"]

    # Weather descriptions
    weather_codes = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light Drizzle",
        61: "Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Snow",
        80: "Rain Showers",
        95: "Thunderstorm"
    }

    condition = weather_codes.get(
        current["weather_code"], "Other Weather Conditions"
    )

    print("\n===================================")
    print("          WEATHER REPORT")
    print("===================================")
    print("City:", city_name)
    print("Country:", country)
    print("Temperature:", current["temperature_2m"], "°C")
    print("Feels Like:", current["apparent_temperature"], "°C")
    print("Humidity:", current["relative_humidity_2m"], "%")
    print("Wind Speed:", current["wind_speed_10m"], "km/h")
    print("Weather:", condition)
    print("===================================")


print("WELCOME TO WEATHER APP")

while True:
    city = input("\nEnter city name: ").strip()

    if not city:
        print("Please enter a city name.")
        continue

    try:
        get_weather(city)
    except requests.exceptions.RequestException:
        print("Network error. Please check your internet connection.")
    except (KeyError, IndexError, ValueError):
        print("Unable to read weather data. Please try again.")

    choice = input("\nCheck another city? (yes/no): ").lower()

    if choice != "yes":
        print("Thank you for using Weather App!")
        break
