from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Convert place name to latitude & longitude
def get_location(place_name):
    location_url = f"https://nominatim.openstreetmap.org/search?format=json&q={place_name}"
    headers = {"User-Agent": "PIX AI"}
    response = requests.get(location_url, headers=headers)
    data = response.json()

    if not data:
        return None, None

    return data[0]["lat"], data[0]["lon"]

# Get weather information using latitude & longitude
def get_weather(latitude, longitude):
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    )
    response = requests.get(weather_url)
    data = response.json()

    if "current" not in data or "temperature_2m" not in data["current"]:
        return None

    return data["current"]["temperature_2m"], data["current"].get("wind_speed_10m")

# Home route
@app.route("/")
def home():
    return jsonify({"status": "running", "message": "Weather API online"})

# Weather route
@app.route("/weather")
def weather():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "place parameter required"}), 400

    lat, lon = get_location(place)
    if not lat:
        return jsonify({"error": "Invalid place"}), 404

    temperature, wind = get_weather(lat, lon)

    if temperature is None:
        return jsonify({"error": "Weather data not available"}), 500

    return jsonify({
        "place": place,
        "temperature_c": temperature,
        "wind_speed": wind,
        "latitude": lat,
        "longitude": lon
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
