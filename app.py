from flask import Flask, request, render_template
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Convert place name to latitude & longitude
def get_location(place_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "format": "json",
        "q": place_name,
        "limit": 1
    }
    headers = {
        "User-Agent": "WeatherApp-Abhinav (your-email@example.com)"
    }

    logging.info(f"Fetching location for: {place_name}")
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        logging.error(f"Nominatim error: {response.status_code}")
        return None, None

    data = response.json()
    if not data:
        return None, None

    return data[0]["lat"], data[0]["lon"]

# Get weather by lat/lon
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m"
    }

    logging.info(f"Fetching weather for: {lat}, {lon}")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        logging.error("Open-Meteo error")
        return None

    data = response.json()
    if "current" not in data:
        return None

    return data["current"]["temperature_2m"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        place = request.form.get("place")
        lat, lon = get_location(place)

        if lat is None:
            result = "Invalid place. Try again."
        else:
            temp = get_weather(lat, lon)
            if temp is None:
                result = "Weather data not available."
            else:
                result = f"The current temperature in {place} is {temp}°C."

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run()
