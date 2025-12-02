from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Convert place name to latitude & longitude
def get_location(place_name):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={place_name}"
    headers = {"User-Agent": "Weather-Web-App"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if not data:
        return None, None
    return data[0]["lat"], data[0]["lon"]

# Get weather by lat/lon
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
    response = requests.get(url)
    data = response.json()
    if "current" not in data:
        return None
    return data["current"]["temperature_2m"]

# Web UI

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

    return render_template_string("index.html", result=result)

if __name__ == "__main__":
    app.run()
