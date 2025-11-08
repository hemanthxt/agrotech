"""Irrigation and water management calculator"""
from typing import Dict
import math

class IrrigationCalculator:
    """Calculate water requirements and irrigation schedules"""
    
    def __init__(self):
        # Crop water requirements (mm per day during peak season)
        self.crop_water_needs = {
            "Rice": 8.0,
            "Sugarcane": 7.5,
            "Banana": 7.0,
            "Cotton": 6.5,
            "Corn": 6.0,
            "Wheat": 5.0,
            "Soybeans": 5.5,
            "Tomatoes": 6.0,
            "Potatoes": 5.0,
            "Onions": 4.5,
            "Cabbage": 5.0,
            "Lettuce": 4.0,
            "Cucumbers": 5.5,
            "Peppers": 5.0,
            "Groundnut": 4.5,
            "Sunflower": 5.5,
            "Mango": 6.0,
            "Grapes": 5.0,
        }
        
        # Crop coefficients for different growth stages
        self.growth_stage_kc = {
            "initial": 0.5,
            "development": 0.75,
            "mid_season": 1.15,
            "late_season": 0.7,
        }
    
    def calculate_water_requirement(self, crop: str, area_acres: float,
                                   growth_stage: str = "mid_season",
                                   temperature: float = 30,
                                   humidity: float = 60,
                                   rainfall_mm: float = 0) -> Dict:
        """Calculate daily water requirement"""
        
        # Base water need (mm/day)
        base_need = self.crop_water_needs.get(crop, 5.0)
        
        # Adjust for growth stage
        kc = self.growth_stage_kc.get(growth_stage, 1.0)
        
        # Temperature adjustment (higher temp = more water)
        temp_factor = 1.0 + ((temperature - 25) * 0.02)
        
        # Humidity adjustment (lower humidity = more water)
        humidity_factor = 1.0 + ((60 - humidity) * 0.01)
        
        # Calculate adjusted water need
        daily_need_mm = base_need * kc * temp_factor * humidity_factor
        
        # Account for rainfall
        irrigation_need_mm = max(0, daily_need_mm - rainfall_mm)
        
        # Convert to volume (1 mm over 1 acre = 4046.86 liters)
        area_sqm = area_acres * 4046.86
        daily_volume_liters = irrigation_need_mm * area_sqm
        
        # Weekly requirement
        weekly_volume_liters = daily_volume_liters * 7
        
        return {
            "crop": crop,
            "area_acres": area_acres,
            "growth_stage": growth_stage,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall_mm": rainfall_mm,
            "daily_need_mm": daily_need_mm,
            "irrigation_need_mm": irrigation_need_mm,
            "daily_volume_liters": daily_volume_liters,
            "weekly_volume_liters": weekly_volume_liters,
            "daily_volume_cubic_meters": daily_volume_liters / 1000,
            "weekly_volume_cubic_meters": weekly_volume_liters / 1000,
        }
    
    def irrigation_schedule(self, crop: str, irrigation_method: str = "drip") -> Dict:
        """Suggest irrigation frequency and duration"""
        
        # Irrigation efficiency by method
        efficiency = {
            "flood": 0.50,
            "furrow": 0.60,
            "sprinkler": 0.75,
            "drip": 0.90,
            "micro_sprinkler": 0.85,
        }
        
        eff = efficiency.get(irrigation_method, 0.70)
        
        # Recommended frequencies
        schedules = {
            "Rice": {"frequency_days": 1, "duration_hours": 2, "method": "flood"},
            "Wheat": {"frequency_days": 7, "duration_hours": 3, "method": "sprinkler"},
            "Cotton": {"frequency_days": 5, "duration_hours": 2, "method": "drip"},
            "Corn": {"frequency_days": 5, "duration_hours": 2.5, "method": "sprinkler"},
            "Tomatoes": {"frequency_days": 3, "duration_hours": 1.5, "method": "drip"},
            "Potatoes": {"frequency_days": 5, "duration_hours": 2, "method": "sprinkler"},
            "Sugarcane": {"frequency_days": 7, "duration_hours": 4, "method": "furrow"},
        }
        
        default = {"frequency_days": 5, "duration_hours": 2, "method": "sprinkler"}
        schedule = schedules.get(crop, default)
        
        return {
            "crop": crop,
            "irrigation_method": irrigation_method,
            "efficiency": eff,
            "recommended_frequency_days": schedule["frequency_days"],
            "recommended_duration_hours": schedule["duration_hours"],
            "best_method": schedule["method"],
            "water_saved_vs_flood": f"{((eff - 0.50) / 0.50 * 100):.0f}%"
        }
    
    def calculate_irrigation_cost(self, volume_liters: float, 
                                 water_source: str = "borewell",
                                 electricity_cost_per_unit: float = 6.0) -> Dict:
        """Calculate cost of irrigation"""
        
        # Pump efficiency and power requirements
        pump_specs = {
            "borewell": {"hp": 5, "efficiency": 0.65, "cost_per_hour": 25},
            "canal": {"hp": 0, "efficiency": 1.0, "cost_per_hour": 5},
            "river": {"hp": 3, "efficiency": 0.70, "cost_per_hour": 15},
            "well": {"hp": 3, "efficiency": 0.70, "cost_per_hour": 15},
            "tank": {"hp": 2, "efficiency": 0.75, "cost_per_hour": 10},
        }
        
        spec = pump_specs.get(water_source, pump_specs["borewell"])
        
        # Estimate pumping time (liters per hour for typical pump)
        pump_rate_lph = 10000  # 10,000 liters per hour
        pumping_hours = volume_liters / pump_rate_lph
        
        # Calculate electricity cost
        if spec["hp"] > 0:
            kw = spec["hp"] * 0.746  # Convert HP to kW
            units_consumed = kw * pumping_hours
            electricity_cost = units_consumed * electricity_cost_per_unit
        else:
            electricity_cost = 0
        
        # Total cost including maintenance
        maintenance_cost = pumping_hours * 5  # Rs 5 per hour maintenance
        total_cost = electricity_cost + maintenance_cost + (spec["cost_per_hour"] * pumping_hours)
        
        return {
            "water_source": water_source,
            "volume_liters": volume_liters,
            "pumping_hours": pumping_hours,
            "electricity_units": units_consumed if spec["hp"] > 0 else 0,
            "electricity_cost": electricity_cost,
            "maintenance_cost": maintenance_cost,
            "total_cost": total_cost,
            "cost_per_1000_liters": (total_cost / volume_liters * 1000) if volume_liters > 0 else 0
        }
    
    def water_conservation_tips(self, crop: str, current_method: str) -> Dict:
        """Provide water-saving recommendations"""
        
        tips = {
            "general": [
                "Irrigate early morning or evening to reduce evaporation",
                "Use mulching to retain soil moisture",
                "Monitor soil moisture before irrigating",
                "Fix leaks in pipes and channels immediately",
                "Use rainwater harvesting systems",
            ],
            "drip": [
                "Check drippers regularly for clogging",
                "Maintain proper pressure in the system",
                "Clean filters weekly",
            ],
            "sprinkler": [
                "Adjust sprinkler height for uniform coverage",
                "Avoid irrigation during windy conditions",
                "Use low-angle sprinklers to reduce drift",
            ],
            "flood": [
                "Consider switching to drip or sprinkler (save 40-50% water)",
                "Level fields properly for uniform water distribution",
                "Use shorter flood durations with more frequency",
            ]
        }
        
        method_tips = tips.get(current_method, [])
        
        savings_potential = {
            "flood": "50%",
            "furrow": "40%",
            "sprinkler": "25%",
            "drip": "10%",
            "micro_sprinkler": "15%"
        }
        
        return {
            "crop": crop,
            "current_method": current_method,
            "general_tips": tips["general"],
            "method_specific_tips": method_tips,
            "potential_water_savings": savings_potential.get(current_method, "20%"),
            "recommended_upgrade": "drip" if current_method in ["flood", "furrow"] else current_method
        }
