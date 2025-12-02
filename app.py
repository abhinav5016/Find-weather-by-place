from flask import Flask, request, render_template
import requests
import logging

app = Flask(__name__)

# Enable logging (shows in Render logs)
logging.basicConfig(level=logging.INFO)

# Convert place name to latitude & longitude
def get_location(place_name):
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={place_name}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        logging.info("Location API response: %s",response.text)
        
        data = response.json()
        
        if not data:
            return None, None
        
        return data[0]["lat"], data[0]["lon"]
    except Exception as e:
        logging.error("Location error: %s", e)
        return None, None

# Get weather by lat/lon
def get_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)

        logging.info("Weather API response: %s", response.text)

        data = response.json()

        if "current_weather" not in data:
            return None

        return data["current_weather"]["temperature"]

    except Exception as e:
        logging.error("Weather error: %s", e)
        return None


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
