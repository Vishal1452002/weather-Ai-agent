import requests
from typing import Dict, Any, List

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def _safe_get_json(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Internal helper for handling network + JSON errors gracefully.
    """
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        return {"error": f"Network error: {e}"}

    if response.status_code != 200:
        return {"error": f"API error: HTTP {response.status_code}"}

    try:
        return response.json()
    except ValueError:
        return {"error": "Failed to parse JSON response from weather API"}


def get_current_weather(lat: float, lon: float) -> Dict[str, Any]:
    """
    Returns the current weather at (lat, lon).
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",
    }

    data = _safe_get_json(BASE_URL, params)

    if "error" in data:
        return data

    current = data.get("current_weather") or {}
    if not current:
        return {"error": "No current weather data returned"}

    return {
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "time": current.get("time"),
    }


def get_daily_forecast(lat: float, lon: float, days: int = 3) -> Dict[str, Any]:
    """
    Returns daily max/min temperature and rain probability for 'days' days.
    """
    if days < 1 or days > 10:
        return {"error": "days must be between 1 and 10"}

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": days,
    }

    data = _safe_get_json(BASE_URL, params)

    if "error" in data:
        return data

    daily = data.get("daily") or {}

    time_list = daily.get("time") or []
    tmax = daily.get("temperature_2m_max") or []
    tmin = daily.get("temperature_2m_min") or []
    rain = daily.get("precipitation_probability_max") or []

    if not time_list:
        return {"error": "No forecast data returned"}

    results: List[Dict[str, Any]] = []

    for i in range(min(len(time_list), days)):
        results.append(
            {
                "date": time_list[i],
                "temp_max": tmax[i] if i < len(tmax) else None,
                "temp_min": tmin[i] if i < len(tmin) else None,
                "precip_prob": rain[i] if i < len(rain) else None,
            }
        )

    return {"days": results}
