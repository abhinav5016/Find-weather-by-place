import requests


#Convert place name to latitude & longitude---
def get_location(place_name):
    location_url = f"https://nominatim.openstreetmap.org/search?format=json&q={place_name}"
    headers = {"User-Agent": "PIX AI"}
    response = requests.get(location_url, headers=headers)
    data = response.json()
    return data[0]['lat'], data[0]['lon']



#Get weather information using latitude & longitude
def get_weather(latitude, longitude):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    response = requests.get(weather_url)
    data = response.json()
    return data['current']['temperature_2m']


#User input 
place = input("Enter a place you want the weather for: ")

lat, lon = get_location(place)
temperature = get_weather(lat, lon)

print(f"The current temperature in {place} is {temperature}°C.")
print("If you want to check another place!")

print("Thank you")