import requests
import json
from datetime import datetime

# Balaton (Siófok környéke) koordinátái
LAT = 46.91
LON = 18.05

def get_surf_data():
    # Szélsebesség (10m), széllökések és szélirány lekérése
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m&current=wind_speed_10m,wind_gusts_10m,wind_direction_10m&timezone=auto"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        result = {
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "unit": "km/h",
            "current": {
                "speed": data['current']['wind_speed_10m'],
                "gust": data['current']['wind_gusts_10m'],
                "direction": data['current']['wind_direction_10m']
            },
            "history": {
                "time": [t.split("T")[1] for t in data['hourly']['time'][-24:]], # Csak az óra:perc
                "speed": data['hourly']['wind_speed_10m'][-24:],
                "gusts": data['hourly']['wind_gusts_10m'][-24:],
                "direction": data['hourly']['wind_direction_10m'][-24:]
            }
        }
        
        with open('surf_data.json', 'w') as f:
            json.dump(result, f, indent=4)
        print("Szuper! Az adatok frissültek.")
    except Exception as e:
        print(f"Hiba történt: {e}")

if __name__ == "__main__":
    get_surf_data()
