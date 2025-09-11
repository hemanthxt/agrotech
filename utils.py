from datetime import datetime
from typing import Dict, Optional, Any

def format_temperature(temp: float, unit: str = "C") -> str:
    """Format temperature with appropriate unit"""
    if unit.upper() == "F":
        temp_f = (temp * 9/5) + 32
        return f"{temp_f:.1f}°F"
    return f"{temp:.1f}°C"

def format_precipitation(precip: float, unit: str = "mm") -> str:
    """Format precipitation with appropriate unit"""
    if unit.lower() == "inches":
        precip_in = precip / 25.4
        return f"{precip_in:.2f} in"
    return f"{precip:.1f} mm"

def get_weather_icon(condition: str) -> str:
    """Get emoji icon for weather condition"""
    icons = {
        "clear": "☀️",
        "sunny": "☀️",
        "cloudy": "☁️",
        "partly_cloudy": "⛅",
        "overcast": "☁️",
        "rain": "🌧️",
        "heavy_rain": "⛈️",
        "snow": "🌨️",
        "fog": "🌫️",
        "wind": "💨",
        "storm": "⛈️"
    }
    return icons.get(condition.lower(), "🌤️")

def calculate_heat_index(temp: float, humidity: float) -> float:
    """Calculate heat index for farmer safety"""
    if temp < 27:  # Heat index only relevant at higher temperatures
        return temp
    
    # Simplified heat index calculation
    hi = temp + (humidity - 40) * 0.1
    return hi

def get_uv_risk_level(uv_index: float) -> str:
    """Get UV risk level for outdoor work"""
    if uv_index < 3:
        return "Low"
    elif uv_index < 6:
        return "Moderate"
    elif uv_index < 8:
        return "High"
    elif uv_index < 11:
        return "Very High"
    else:
        return "Extreme"

def format_wind_direction(degrees: float) -> str:
    """Convert wind direction degrees to compass direction"""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    
    # Normalize degrees to 0-360
    degrees = degrees % 360
    
    # Calculate index (16 directions, so 360/16 = 22.5 degrees per direction)
    index = round(degrees / 22.5) % 16
    
    return directions[index]

def is_spraying_weather(wind_speed: float, humidity: float, temp: float) -> Dict[str, Any]:
    """Determine if weather is suitable for spraying operations"""
    suitable = True
    reasons = []
    
    # Wind speed check (ideal: 3-15 km/h)
    if wind_speed > 15:
        suitable = False
        reasons.append(f"Wind too strong ({wind_speed:.1f} km/h) - drift risk")
    elif wind_speed < 3:
        reasons.append("Very low wind - may affect coverage")
    
    # Temperature check (avoid extreme heat)
    if temp > 30:
        suitable = False
        reasons.append(f"Temperature too high ({temp:.1f}°C) - evaporation risk")
    elif temp < 5:
        suitable = False
        reasons.append(f"Temperature too low ({temp:.1f}°C) - poor uptake")
    
    # Humidity check (ideal: 50-90%)
    if humidity < 50:
        suitable = False
        reasons.append(f"Humidity too low ({humidity:.0f}%) - poor coverage")
    elif humidity > 95:
        suitable = False
        reasons.append(f"Humidity too high ({humidity:.0f}%) - runoff risk")
    
    return {
        "suitable": suitable,
        "reasons": reasons if reasons else ["Good conditions for spraying"]
    }

def calculate_growing_degree_days(temp_max: float, temp_min: float, base_temp: float = 10) -> float:
    """Calculate growing degree days for crop development tracking"""
    avg_temp = (temp_max + temp_min) / 2
    
    # Standard GDD calculation
    gdd = max(0, avg_temp - base_temp)
    
    return gdd

def format_datetime_local(iso_string: str) -> str:
    """Format ISO datetime string to local readable format"""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime("%m/%d %H:%M")
    except:
        return iso_string

def get_irrigation_timing_advice(humidity: float, temp: float, wind_speed: float) -> str:
    """Provide irrigation timing advice based on weather"""
    if temp > 30 and humidity < 40:
        return "Early morning irrigation recommended to reduce evaporation"
    elif wind_speed > 20:
        return "Avoid irrigation during high winds to prevent uneven distribution"
    elif humidity > 90:
        return "Delay irrigation - high humidity may promote disease"
    else:
        return "Good conditions for irrigation"
