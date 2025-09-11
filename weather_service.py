import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st

class WeatherService:
    """Service for fetching weather data from Open-Meteo API"""
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1"
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_current_weather(_self, latitude: float, longitude: float) -> Optional[Dict]:
        """Fetch current weather conditions"""
        try:
            url = f"{_self.base_url}/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m", 
                    "precipitation",
                    "wind_speed_10m",
                    "wind_direction_10m"
                ],
                "timezone": "auto"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data["current"]
            return {
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "precipitation": current["precipitation"],
                "wind_speed": current["wind_speed_10m"],
                "wind_direction": current["wind_direction_10m"],
                "timestamp": current["time"]
            }
            
        except Exception as e:
            st.error(f"Error fetching current weather: {str(e)}")
            return None
    
    @st.cache_data(ttl=300)
    def get_daily_forecast(_self, latitude: float, longitude: float, days: int = 7) -> Optional[List[Dict]]:
        """Fetch daily weather forecast"""
        try:
            url = f"{_self.base_url}/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "wind_speed_10m_max",
                    "relative_humidity_2m_mean"
                ],
                "forecast_days": days,
                "timezone": "auto"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            daily = data["daily"]
            forecast = []
            
            for i in range(len(daily["time"])):
                forecast.append({
                    "date": daily["time"][i],
                    "temp_max": daily["temperature_2m_max"][i],
                    "temp_min": daily["temperature_2m_min"][i],
                    "precipitation": daily["precipitation_sum"][i],
                    "wind_speed": daily["wind_speed_10m_max"][i],
                    "humidity": daily["relative_humidity_2m_mean"][i]
                })
            
            return forecast
            
        except Exception as e:
            st.error(f"Error fetching daily forecast: {str(e)}")
            return None
    
    @st.cache_data(ttl=300)
    def get_hourly_forecast(_self, latitude: float, longitude: float, hours: int = 24) -> Optional[List[Dict]]:
        """Fetch hourly weather forecast"""
        try:
            url = f"{_self.base_url}/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation",
                    "wind_speed_10m"
                ],
                "forecast_hours": hours,
                "timezone": "auto"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            hourly = data["hourly"]
            forecast = []
            
            for i in range(len(hourly["time"])):
                forecast.append({
                    "time": hourly["time"][i],
                    "temperature": hourly["temperature_2m"][i],
                    "humidity": hourly["relative_humidity_2m"][i],
                    "precipitation": hourly["precipitation"][i],
                    "wind_speed": hourly["wind_speed_10m"][i]
                })
            
            return forecast
            
        except Exception as e:
            st.error(f"Error fetching hourly forecast: {str(e)}")
            return None
    
    def check_weather_alerts(self, current_weather: Dict, daily_forecast: Dict) -> List[Dict]:
        """Check for weather conditions that might affect crops"""
        alerts = []
        
        # Temperature alerts
        if current_weather["temperature"] < 0:
            alerts.append({
                "type": "Frost Warning",
                "message": "Freezing temperatures detected. Protect sensitive crops immediately.",
                "severity": "error"
            })
        elif current_weather["temperature"] < 5:
            alerts.append({
                "type": "Cold Warning",
                "message": "Low temperatures may slow crop growth and increase disease risk.",
                "severity": "warning"
            })
        elif current_weather["temperature"] > 35:
            alerts.append({
                "type": "Heat Stress",
                "message": "High temperatures may stress crops. Ensure adequate irrigation.",
                "severity": "warning"
            })
        
        # Wind alerts
        if current_weather["wind_speed"] > 50:
            alerts.append({
                "type": "High Wind Warning",
                "message": "Strong winds may damage crops and affect spraying operations.",
                "severity": "warning"
            })
        
        # Precipitation alerts
        if daily_forecast["precipitation"] > 25:
            alerts.append({
                "type": "Heavy Rain Expected",
                "message": "Heavy rainfall forecasted. Avoid field operations and monitor for waterlogging.",
                "severity": "warning"
            })
        elif daily_forecast["precipitation"] == 0 and current_weather["humidity"] < 30:
            alerts.append({
                "type": "Dry Conditions",
                "message": "Low humidity and no precipitation. Consider irrigation needs.",
                "severity": "info"
            })
        
        # Humidity alerts
        if current_weather["humidity"] > 90:
            alerts.append({
                "type": "High Humidity",
                "message": "Very high humidity increases disease risk. Monitor crops closely.",
                "severity": "warning"
            })
        
        return alerts
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour since location names don't change frequently
    def get_location_name(_self, latitude: float, longitude: float) -> Optional[str]:
        """Get location name from coordinates using reverse geocoding"""
        try:
            # Use a simple reverse geocoding API to get location name
            url = "https://api.bigdatacloud.net/data/reverse-geocode-client"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "localityLanguage": "en"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract location components
            city = data.get('city', '')
            locality = data.get('locality', '')
            administrative_area = data.get('principalSubdivision', '')
            country = data.get('countryName', '')
            
            # Build location name with available components
            location_parts = []
            
            if city:
                location_parts.append(city)
            elif locality:
                location_parts.append(locality)
            
            if administrative_area and administrative_area != city:
                location_parts.append(administrative_area)
            
            if country and len(location_parts) < 2:
                location_parts.append(country)
            
            if location_parts:
                return ", ".join(location_parts[:3])  # Limit to 3 components max
            else:
                return f"Location ({latitude:.2f}, {longitude:.2f})"
                
        except Exception as e:
            st.warning(f"Could not detect location name: {str(e)}")
            return f"Farm Location ({latitude:.2f}, {longitude:.2f})"
    
    @st.cache_data(ttl=3600)
    def search_locations(_self, query: str) -> List[Dict]:
        """Search for locations using geocoding API"""
        if not query or len(query) < 2:
            return []
        
        try:
            # Use OpenStreetMap Nominatim for location search
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": query,
                "format": "json",
                "limit": 8,
                "addressdetails": 1,
                "extratags": 1
            }
            
            headers = {
                'User-Agent': 'Agricultural-Assistant/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            locations = []
            for item in data:
                # Extract relevant information
                display_name = item.get('display_name', '')
                lat = float(item.get('lat', 0))
                lon = float(item.get('lon', 0))
                
                # Build clean location name
                address = item.get('address', {})
                city = address.get('city', address.get('town', address.get('village', '')))
                state = address.get('state', address.get('region', ''))
                country = address.get('country', '')
                
                # Create a clean, readable location name
                location_parts = []
                if city:
                    location_parts.append(city)
                if state and state != city:
                    location_parts.append(state)
                if country and len(location_parts) < 2:
                    location_parts.append(country)
                
                clean_name = ", ".join(location_parts[:3]) if location_parts else display_name
                
                locations.append({
                    'name': clean_name,
                    'display_name': display_name,
                    'latitude': lat,
                    'longitude': lon,
                    'address': address
                })
            
            return locations
            
        except Exception as e:
            st.warning(f"Location search failed: {str(e)}")
            return []
    
    @st.cache_data(ttl=3600)
    def get_coordinates_from_location(_self, location_name: str) -> Optional[Dict]:
        """Get coordinates from location name"""
        locations = _self.search_locations(location_name)
        if locations:
            return {
                'latitude': locations[0]['latitude'],
                'longitude': locations[0]['longitude'],
                'name': locations[0]['name'],
                'display_name': locations[0]['display_name']
            }
        return None
