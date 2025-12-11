import requests

def get_coordinates(city_name: str):
    """
    Returns latitude and longitude for ANY city using Open-Meteo geocoding API.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name}

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"error": f"Geocoding API error: {response.status_code}"}

        data = response.json()

        # If no results found
        if "results" not in data or len(data["results"]) == 0:
            return {"error": "City not found"}

        result = data["results"][0]

        return {
            "lat": result["latitude"],
            "lon": result["longitude"],
            "city": result["name"],
            "country": result.get("country", "")
        }

    except Exception as e:
        return {"error": str(e)}
