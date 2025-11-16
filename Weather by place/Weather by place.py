import requests


# Convert place name to latitude & longitude------------------------
def get_location(place_name):
    location_url = (
        f"https://nominatim.openstreetmap.org/search?format=json&q={place_name}"
    )
    headers = {"User-Agent": "PIX AI"}
    response = requests.get(location_url, headers=headers)
    data = response.json()

    # If API finds no matching place
    if not data:
        return None, None

    return data[0]["lat"], data[0]["lon"]


# Get weather information using latitude & longitude----------------
def get_weather(latitude, longitude):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    response = requests.get(weather_url)
    data = response.json()

    # if missing
    if "current" not in data or "temperature_2m" not in data["current"]:
        return None

    return data["current"]["temperature_2m"]


print("Hello there...Nice to meet you")

# User input & loop function-----------------------------------------
while True:
    place = input("Enter a place you want the weather for: ")

    lat, lon = get_location(place)

    # if no valid locations found
    if lat is None:
        print("No place found.Please enter a valid location.\n")
        continue

    temperature = get_weather(lat, lon)

    # If weather data not found
    if temperature is None:
        print("Weather data not available for this place.\n")
        continue

    print(f"The current temperature in {place} is {temperature}°C.")

    # Asking user if they want to continue
    again = input("Do you want to check another place? (yes/no): ")

    if again.lower() != "yes":
        print("Okay! Thankyou for using PIX weather ai.")
        break


print()
