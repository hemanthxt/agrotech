from typing import Dict, List
import streamlit as st

class CropRecommendations:
    """Service for providing crop-specific recommendations based on weather conditions"""
    
    def __init__(self):
        # Crop requirements database
        self.crop_requirements = {
            "Wheat": {
                "temp_range": (10, 24),
                "optimal_temp": (15, 20),
                "humidity_range": (50, 70),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Corn": {
                "temp_range": (18, 30),
                "optimal_temp": (21, 27),
                "humidity_range": (60, 80),
                "water_needs": "high",
                "sensitive_stages": ["germination", "flowering"]
            },
            "Rice": {
                "temp_range": (20, 35),
                "optimal_temp": (25, 30),
                "humidity_range": (70, 90),
                "water_needs": "very_high",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Soybeans": {
                "temp_range": (15, 30),
                "optimal_temp": (20, 25),
                "humidity_range": (60, 75),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Tomatoes": {
                "temp_range": (18, 27),
                "optimal_temp": (21, 24),
                "humidity_range": (65, 85),
                "water_needs": "high",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Potatoes": {
                "temp_range": (15, 20),
                "optimal_temp": (16, 18),
                "humidity_range": (80, 90),
                "water_needs": "moderate",
                "sensitive_stages": ["vegetative", "fruiting"]
            },
            "Cotton": {
                "temp_range": (20, 35),
                "optimal_temp": (25, 30),
                "humidity_range": (50, 70),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Lettuce": {
                "temp_range": (7, 24),
                "optimal_temp": (15, 18),
                "humidity_range": (80, 95),
                "water_needs": "high",
                "sensitive_stages": ["vegetative"]
            },
            "Carrots": {
                "temp_range": (16, 18),
                "optimal_temp": (16, 18),
                "humidity_range": (80, 90),
                "water_needs": "moderate",
                "sensitive_stages": ["germination", "vegetative"]
            },
            "Onions": {
                "temp_range": (12, 24),
                "optimal_temp": (15, 20),
                "humidity_range": (65, 75),
                "water_needs": "moderate",
                "sensitive_stages": ["vegetative", "maturation"]
            },
            "Cucumbers": {
                "temp_range": (18, 30),
                "optimal_temp": (21, 27),
                "humidity_range": (65, 85),
                "water_needs": "high",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Peppers": {
                "temp_range": (20, 30),
                "optimal_temp": (24, 27),
                "humidity_range": (60, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Spinach": {
                "temp_range": (7, 20),
                "optimal_temp": (10, 16),
                "humidity_range": (75, 95),
                "water_needs": "moderate",
                "sensitive_stages": ["vegetative"]
            },
            "Broccoli": {
                "temp_range": (15, 20),
                "optimal_temp": (16, 18),
                "humidity_range": (80, 90),
                "water_needs": "high",
                "sensitive_stages": ["vegetative", "flowering"]
            },
            "Cabbage": {
                "temp_range": (13, 24),
                "optimal_temp": (15, 20),
                "humidity_range": (80, 90),
                "water_needs": "moderate",
                "sensitive_stages": ["vegetative"]
            },
            "Beans": {
                "temp_range": (18, 30),
                "optimal_temp": (21, 27),
                "humidity_range": (65, 75),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Peas": {
                "temp_range": (7, 18),
                "optimal_temp": (13, 16),
                "humidity_range": (70, 85),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Squash": {
                "temp_range": (20, 32),
                "optimal_temp": (24, 29),
                "humidity_range": (65, 80),
                "water_needs": "high",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Eggplant": {
                "temp_range": (21, 30),
                "optimal_temp": (24, 27),
                "humidity_range": (65, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Radishes": {
                "temp_range": (10, 18),
                "optimal_temp": (13, 16),
                "humidity_range": (75, 90),
                "water_needs": "moderate",
                "sensitive_stages": ["germination", "vegetative"]
            },
            "Cauliflower": {
                "temp_range": (15, 20),
                "optimal_temp": (16, 18),
                "humidity_range": (80, 90),
                "water_needs": "high",
                "sensitive_stages": ["vegetative", "flowering"]
            },
            "Okra": {
                "temp_range": (25, 35),
                "optimal_temp": (27, 32),
                "humidity_range": (65, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Beetroot": {
                "temp_range": (15, 20),
                "optimal_temp": (16, 18),
                "humidity_range": (80, 90),
                "water_needs": "moderate",
                "sensitive_stages": ["germination", "vegetative"]
            },
            "Turnip": {
                "temp_range": (10, 18),
                "optimal_temp": (13, 16),
                "humidity_range": (75, 85),
                "water_needs": "moderate",
                "sensitive_stages": ["vegetative"]
            },
            "Ginger": {
                "temp_range": (20, 30),
                "optimal_temp": (24, 27),
                "humidity_range": (75, 90),
                "water_needs": "high",
                "sensitive_stages": ["planting", "vegetative"]
            },
            "Garlic": {
                "temp_range": (12, 25),
                "optimal_temp": (15, 20),
                "humidity_range": (65, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["vegetative", "maturation"]
            },
            "Coriander": {
                "temp_range": (17, 27),
                "optimal_temp": (20, 24),
                "humidity_range": (60, 75),
                "water_needs": "moderate",
                "sensitive_stages": ["vegetative"]
            },
            "Mint": {
                "temp_range": (15, 25),
                "optimal_temp": (18, 22),
                "humidity_range": (70, 85),
                "water_needs": "high",
                "sensitive_stages": ["vegetative"]
            },
            "Fenugreek": {
                "temp_range": (15, 25),
                "optimal_temp": (18, 22),
                "humidity_range": (60, 75),
                "water_needs": "moderate",
                "sensitive_stages": ["germination", "vegetative"]
            },
            "Mustard": {
                "temp_range": (10, 25),
                "optimal_temp": (15, 20),
                "humidity_range": (60, 75),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Green Chili": {
                "temp_range": (20, 30),
                "optimal_temp": (24, 28),
                "humidity_range": (65, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Turmeric": {
                "temp_range": (20, 30),
                "optimal_temp": (24, 27),
                "humidity_range": (70, 85),
                "water_needs": "high",
                "sensitive_stages": ["planting", "vegetative"]
            },
            "Sugarcane": {
                "temp_range": (20, 40),
                "optimal_temp": (26, 32),
                "humidity_range": (70, 90),
                "water_needs": "very_high",
                "sensitive_stages": ["planting", "vegetative", "maturation"]
            },
            "Banana": {
                "temp_range": (26, 30),
                "optimal_temp": (27, 29),
                "humidity_range": (75, 85),
                "water_needs": "high",
                "sensitive_stages": ["planting", "flowering", "fruiting"]
            },
            "Mango": {
                "temp_range": (24, 30),
                "optimal_temp": (25, 28),
                "humidity_range": (70, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Apple": {
                "temp_range": (21, 24),
                "optimal_temp": (21, 23),
                "humidity_range": (70, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Grapes": {
                "temp_range": (15, 25),
                "optimal_temp": (18, 22),
                "humidity_range": (60, 75),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Orange": {
                "temp_range": (13, 37),
                "optimal_temp": (15, 30),
                "humidity_range": (65, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Coconut": {
                "temp_range": (27, 35),
                "optimal_temp": (28, 32),
                "humidity_range": (70, 90),
                "water_needs": "high",
                "sensitive_stages": ["planting", "flowering"]
            },
            "Cashew": {
                "temp_range": (20, 30),
                "optimal_temp": (24, 28),
                "humidity_range": (70, 85),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Groundnut": {
                "temp_range": (20, 30),
                "optimal_temp": (24, 28),
                "humidity_range": (65, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            },
            "Sesame": {
                "temp_range": (25, 30),
                "optimal_temp": (26, 28),
                "humidity_range": (60, 75),
                "water_needs": "low",
                "sensitive_stages": ["flowering", "maturation"]
            },
            "Sunflower": {
                "temp_range": (20, 25),
                "optimal_temp": (21, 24),
                "humidity_range": (60, 70),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "maturation"]
            },
            "Safflower": {
                "temp_range": (16, 25),
                "optimal_temp": (18, 22),
                "humidity_range": (55, 70),
                "water_needs": "low",
                "sensitive_stages": ["flowering", "maturation"]
            },
            "Castor": {
                "temp_range": (20, 30),
                "optimal_temp": (24, 28),
                "humidity_range": (65, 80),
                "water_needs": "moderate",
                "sensitive_stages": ["flowering", "fruiting"]
            }
        }
    
    def get_recommendations(self, crop_type: str, growth_stage: str, 
                          current_weather: Dict, daily_forecast: Dict) -> Dict:
        """Generate comprehensive recommendations for the crop"""
        
        crop_data = self.crop_requirements.get(crop_type, {})
        if not crop_data:
            return self._default_recommendations()
        
        recommendations = {
            "irrigation": self._get_irrigation_advice(crop_type, growth_stage, current_weather, daily_forecast),
            "activities": self._get_field_activities(crop_type, growth_stage, current_weather),
            "disease_risk": self._assess_disease_risk(crop_type, current_weather),
            "general_advice": self._get_general_advice(crop_type, growth_stage, current_weather, daily_forecast)
        }
        
        return recommendations
    
    def _get_irrigation_advice(self, crop_type: str, growth_stage: str, 
                              current_weather: Dict, daily_forecast: Dict) -> Dict:
        """Determine irrigation needs"""
        crop_data = self.crop_requirements[crop_type]
        
        # Base water needs by crop
        water_needs_multiplier = {
            "very_high": 1.5,
            "high": 1.2,
            "moderate": 1.0,
            "low": 0.8
        }
        
        base_need = water_needs_multiplier.get(crop_data["water_needs"], 1.0)
        
        # Adjust for temperature
        temp_factor = 1.0
        if current_weather["temperature"] > crop_data["optimal_temp"][1]:
            temp_factor = 1.3
        elif current_weather["temperature"] < crop_data["optimal_temp"][0]:
            temp_factor = 0.8
        
        # Adjust for humidity
        humidity_factor = 1.0
        if current_weather["humidity"] < 50:
            humidity_factor = 1.2
        elif current_weather["humidity"] > 80:
            humidity_factor = 0.8
        
        # Consider recent precipitation
        recent_rain = daily_forecast["precipitation"]
        rain_factor = max(0.3, 1.0 - (recent_rain / 10))
        
        # Growth stage sensitivity
        stage_factor = 1.0
        sensitive_stages = crop_data.get("sensitive_stages", [])
        if growth_stage.lower() in sensitive_stages:
            stage_factor = 1.2
        
        irrigation_need = base_need * temp_factor * humidity_factor * rain_factor * stage_factor
        
        if irrigation_need > 1.2:
            return {
                "needed": True,
                "message": f"Irrigation recommended. High water demand due to weather conditions."
            }
        elif irrigation_need > 0.8:
            return {
                "needed": True,
                "message": f"Moderate irrigation needed. Monitor soil moisture closely."
            }
        else:
            return {
                "needed": False,
                "message": f"Irrigation not immediately needed. Recent rainfall sufficient."
            }
    
    def _get_field_activities(self, crop_type: str, growth_stage: str, current_weather: Dict) -> List[Dict]:
        """Recommend field activities based on weather"""
        activities = []
        
        # Spraying conditions
        wind_speed = current_weather["wind_speed"]
        humidity = current_weather["humidity"]
        
        if wind_speed < 15 and humidity > 50:
            activities.append({
                "activity": "Pesticide/Fungicide Application",
                "recommended": True,
                "reason": "Good conditions - low wind and adequate humidity"
            })
        else:
            reason = "Poor conditions - "
            if wind_speed >= 15:
                reason += "high wind (drift risk), "
            if humidity <= 50:
                reason += "low humidity (poor coverage)"
            activities.append({
                "activity": "Pesticide/Fungicide Application",
                "recommended": False,
                "reason": reason.rstrip(", ")
            })
        
        # Harvesting conditions
        temp = current_weather["temperature"]
        if growth_stage.lower() == "harvest":
            if humidity < 75 and temp > 10:
                activities.append({
                    "activity": "Harvesting",
                    "recommended": True,
                    "reason": "Good conditions - low humidity and adequate temperature"
                })
            else:
                activities.append({
                    "activity": "Harvesting",
                    "recommended": False,
                    "reason": "Wait for drier conditions to prevent quality issues"
                })
        
        # Planting conditions
        if growth_stage.lower() == "planting":
            crop_data = self.crop_requirements[crop_type]
            temp_range = crop_data["temp_range"]
            
            if temp_range[0] <= temp <= temp_range[1] and humidity > 60:
                activities.append({
                    "activity": "Planting/Seeding",
                    "recommended": True,
                    "reason": "Optimal temperature and moisture conditions"
                })
            else:
                activities.append({
                    "activity": "Planting/Seeding",
                    "recommended": False,
                    "reason": "Temperature or moisture conditions not optimal"
                })
        
        # Fertilizer application
        if wind_speed < 20 and current_weather["precipitation"] < 1:
            activities.append({
                "activity": "Fertilizer Application",
                "recommended": True,
                "reason": "Good conditions - no rain forecast and low wind"
            })
        else:
            activities.append({
                "activity": "Fertilizer Application",
                "recommended": False,
                "reason": "Risk of nutrient runoff or drift"
            })
        
        return activities
    
    def _assess_disease_risk(self, crop_type: str, current_weather: Dict) -> Dict:
        """Assess disease risk based on weather conditions"""
        temp = current_weather["temperature"]
        humidity = current_weather["humidity"]
        
        # General disease risk factors
        risk_score = 0
        
        # High humidity increases fungal disease risk
        if humidity > 85:
            risk_score += 3
        elif humidity > 70:
            risk_score += 2
        elif humidity > 60:
            risk_score += 1
        
        # Temperature in disease-favorable range
        if 15 <= temp <= 25:
            risk_score += 2
        elif 10 <= temp <= 30:
            risk_score += 1
        
        # Wet conditions
        if current_weather["precipitation"] > 0:
            risk_score += 1
        
        if risk_score >= 5:
            return {
                "level": "High",
                "message": "Conditions highly favorable for disease development. Consider preventive treatments."
            }
        elif risk_score >= 3:
            return {
                "level": "Medium",
                "message": "Moderate disease risk. Monitor crops closely for early signs."
            }
        else:
            return {
                "level": "Low",
                "message": "Low disease pressure. Continue regular monitoring."
            }
    
    def _get_general_advice(self, crop_type: str, growth_stage: str, 
                           current_weather: Dict, daily_forecast: Dict) -> List[str]:
        """Generate general farming advice"""
        advice = []
        crop_data = self.crop_requirements[crop_type]
        temp = current_weather["temperature"]
        optimal_temp = crop_data["optimal_temp"]
        
        # Temperature advice
        if temp < optimal_temp[0]:
            advice.append(f"Temperature below optimal range for {crop_type}. Growth may be slower than expected.")
        elif temp > optimal_temp[1]:
            advice.append(f"Temperature above optimal range. Consider shade protection or increased irrigation.")
        else:
            advice.append(f"Temperature is optimal for {crop_type} growth.")
        
        # Growth stage specific advice
        stage_advice = {
            "planting": "Ensure soil temperature is adequate and moisture is sufficient for germination.",
            "germination": "Maintain consistent soil moisture. Avoid field traffic to prevent compaction.",
            "vegetative": "Monitor for nutrient deficiencies. This is a critical growth period.",
            "flowering": "Avoid stress conditions. Ensure adequate water and nutrients.",
            "fruiting": "Critical period for yield determination. Maintain optimal growing conditions.",
            "maturation": "Reduce irrigation gradually. Monitor for harvest readiness.",
            "harvest": "Choose dry conditions for harvest to maintain crop quality."
        }
        
        if growth_stage.lower() in stage_advice:
            advice.append(stage_advice[growth_stage.lower()])
        
        # Weather pattern advice
        if daily_forecast["precipitation"] > 15:
            advice.append("Heavy rain expected. Ensure proper drainage and avoid field operations.")
        
        if current_weather["wind_speed"] > 25:
            advice.append("Strong winds may cause physical damage. Check for lodging in tall crops.")
        
        return advice
    
    def analyze_growing_conditions(self, crop_type: str, current_weather: Dict, daily_forecast: List[Dict]) -> Dict:
        """Analyze overall growing conditions"""
        crop_data = self.crop_requirements.get(crop_type, {})
        if not crop_data:
            return {"overall": "Unknown", "temperature": "Unknown", "moisture": "Unknown"}
        
        temp = current_weather["temperature"]
        optimal_temp = crop_data["optimal_temp"]
        humidity = current_weather["humidity"]
        
        # Temperature analysis
        if optimal_temp[0] <= temp <= optimal_temp[1]:
            temp_status = "Optimal"
        elif crop_data["temp_range"][0] <= temp <= crop_data["temp_range"][1]:
            temp_status = "Good"
        else:
            temp_status = "Suboptimal"
        
        # Moisture analysis
        if crop_data["humidity_range"][0] <= humidity <= crop_data["humidity_range"][1]:
            moisture_status = "Good"
        elif humidity < crop_data["humidity_range"][0]:
            moisture_status = "Dry"
        else:
            moisture_status = "Wet"
        
        # Overall assessment
        if temp_status == "Optimal" and moisture_status == "Good":
            overall = "Excellent"
            trend = "↗️"
        elif temp_status in ["Optimal", "Good"] and moisture_status == "Good":
            overall = "Good"
            trend = "→"
        elif temp_status == "Suboptimal" or moisture_status != "Good":
            overall = "Fair"
            trend = "↘️"
        else:
            overall = "Poor"
            trend = "↓"
        
        return {
            "overall": overall,
            "overall_trend": trend,
            "temperature": temp_status,
            "moisture": moisture_status
        }
    
    def _default_recommendations(self) -> Dict:
        """Default recommendations when crop data is not available"""
        return {
            "irrigation": {
                "needed": False,
                "message": "Monitor soil moisture and local conditions"
            },
            "activities": [
                {
                    "activity": "General Farm Activities",
                    "recommended": True,
                    "reason": "Check current weather conditions before proceeding"
                }
            ],
            "disease_risk": {
                "level": "Medium",
                "message": "Monitor crops regularly for disease symptoms"
            },
            "general_advice": [
                "Consult local agricultural extension services for crop-specific advice",
                "Monitor weather forecasts regularly",
                "Keep detailed records of weather and crop conditions"
            ]
        }
