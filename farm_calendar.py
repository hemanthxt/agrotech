"""Farm calendar and crop scheduling system"""
from datetime import datetime, timedelta
from typing import Dict, List

class FarmCalendar:
    """Manage planting schedules, growth stages, and harvest timing"""
    
    def __init__(self):
        # Crop duration and stages (in days)
        self.crop_schedules = {
            "Wheat": {
                "total_days": 120,
                "stages": {
                    "preparation": 7,
                    "sowing": 3,
                    "germination": 10,
                    "vegetative": 40,
                    "flowering": 20,
                    "grain_filling": 25,
                    "maturation": 15
                },
                "best_sowing_months": [10, 11, 12],  # Oct-Dec
            },
            "Rice": {
                "total_days": 130,
                "stages": {
                    "nursery": 25,
                    "transplanting": 5,
                    "tillering": 30,
                    "flowering": 30,
                    "grain_filling": 30,
                    "maturation": 10
                },
                "best_sowing_months": [6, 7, 8],  # Jun-Aug
            },
            "Corn": {
                "total_days": 100,
                "stages": {
                    "preparation": 7,
                    "sowing": 2,
                    "germination": 8,
                    "vegetative": 35,
                    "flowering": 20,
                    "grain_filling": 20,
                    "maturation": 8
                },
                "best_sowing_months": [2, 3, 7, 8],
            },
            "Cotton": {
                "total_days": 180,
                "stages": {
                    "preparation": 10,
                    "sowing": 3,
                    "germination": 10,
                    "vegetative": 50,
                    "flowering": 40,
                    "boll_development": 50,
                    "maturation": 17
                },
                "best_sowing_months": [4, 5, 6],
            },
            "Tomatoes": {
                "total_days": 90,
                "stages": {
                    "nursery": 25,
                    "transplanting": 5,
                    "vegetative": 25,
                    "flowering": 15,
                    "fruiting": 15,
                    "harvest": 5
                },
                "best_sowing_months": [1, 2, 7, 8, 9],
            },
            "Potatoes": {
                "total_days": 90,
                "stages": {
                    "preparation": 7,
                    "planting": 2,
                    "sprouting": 10,
                    "vegetative": 35,
                    "tuber_formation": 25,
                    "maturation": 11
                },
                "best_sowing_months": [10, 11, 1],
            },
            "Soybeans": {
                "total_days": 110,
                "stages": {
                    "preparation": 7,
                    "sowing": 2,
                    "germination": 8,
                    "vegetative": 40,
                    "flowering": 20,
                    "pod_development": 25,
                    "maturation": 8
                },
                "best_sowing_months": [6, 7],
            },
            "Sugarcane": {
                "total_days": 360,
                "stages": {
                    "preparation": 15,
                    "planting": 5,
                    "germination": 30,
                    "tillering": 60,
                    "grand_growth": 150,
                    "maturation": 100
                },
                "best_sowing_months": [2, 3, 9, 10],
            },
            "Onions": {
                "total_days": 120,
                "stages": {
                    "nursery": 30,
                    "transplanting": 5,
                    "vegetative": 45,
                    "bulb_formation": 30,
                    "maturation": 10
                },
                "best_sowing_months": [10, 11, 12],
            },
        }
    
    def create_schedule(self, crop: str, planting_date: datetime = None) -> Dict:
        """Create a complete farming schedule from planting to harvest"""
        
        if crop not in self.crop_schedules:
            return {"error": f"Crop '{crop}' not found in database"}
        
        if planting_date is None:
            planting_date = datetime.now()
        
        schedule_data = self.crop_schedules[crop]
        stages = schedule_data["stages"]
        
        # Calculate dates for each stage
        current_date = planting_date
        timeline = []
        
        for stage_name, duration_days in stages.items():
            start_date = current_date
            end_date = current_date + timedelta(days=duration_days)
            
            timeline.append({
                "stage": stage_name.replace("_", " ").title(),
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "duration_days": duration_days,
                "activities": self._get_stage_activities(crop, stage_name)
            })
            
            current_date = end_date
        
        harvest_date = current_date
        
        return {
            "crop": crop,
            "planting_date": planting_date.strftime("%Y-%m-%d"),
            "harvest_date": harvest_date.strftime("%Y-%m-%d"),
            "total_duration_days": schedule_data["total_days"],
            "timeline": timeline,
            "best_months": self._month_names(schedule_data["best_sowing_months"])
        }
    
    def _get_stage_activities(self, crop: str, stage: str) -> List[str]:
        """Get recommended activities for each growth stage"""
        
        activities = {
            "preparation": [
                "Plow the field thoroughly",
                "Apply organic manure/compost",
                "Level the field",
                "Prepare seed bed"
            ],
            "sowing": [
                "Use certified quality seeds",
                "Treat seeds with fungicide",
                "Maintain proper spacing",
                "Ensure adequate soil moisture"
            ],
            "planting": [
                "Plant at recommended depth",
                "Water immediately after planting",
                "Use certified planting material"
            ],
            "nursery": [
                "Prepare nursery beds",
                "Maintain proper spacing",
                "Water regularly",
                "Protect from pests"
            ],
            "germination": [
                "Maintain consistent soil moisture",
                "Protect from birds and pests",
                "Monitor emergence rate"
            ],
            "sprouting": [
                "Keep soil moist",
                "Watch for early pests",
                "Remove weak sprouts"
            ],
            "transplanting": [
                "Select healthy seedlings",
                "Transplant in evening hours",
                "Water immediately",
                "Maintain proper spacing"
            ],
            "vegetative": [
                "Apply nitrogen fertilizer",
                "Regular weeding",
                "Irrigate as per schedule",
                "Monitor for pests and diseases"
            ],
            "tillering": [
                "Apply top-dress fertilizer",
                "Maintain water level",
                "Control weeds"
            ],
            "flowering": [
                "Ensure adequate water supply",
                "Protect from extreme weather",
                "Monitor for pests",
                "Avoid nitrogen fertilizer"
            ],
            "fruiting": [
                "Regular irrigation",
                "Apply potash fertilizer",
                "Support heavy fruits if needed",
                "Monitor fruit development"
            ],
            "boll_development": [
                "Regular irrigation",
                "Monitor for bollworm",
                "Remove damaged bolls"
            ],
            "pod_development": [
                "Ensure adequate moisture",
                "Monitor for pod borer",
                "Avoid excessive nitrogen"
            ],
            "grain_filling": [
                "Maintain moisture levels",
                "Protect from birds",
                "Monitor grain development"
            ],
            "tuber_formation": [
                "Ridge up the soil",
                "Regular irrigation",
                "Monitor for tuber size"
            ],
            "bulb_formation": [
                "Reduce irrigation gradually",
                "Stop nitrogen application",
                "Monitor bulb size"
            ],
            "maturation": [
                "Reduce irrigation",
                "Monitor crop maturity",
                "Prepare for harvest"
            ],
            "grand_growth": [
                "Heavy irrigation required",
                "Regular fertilization",
                "Remove unwanted shoots"
            ],
            "harvest": [
                "Choose right weather",
                "Use proper harvesting tools",
                "Handle produce carefully",
                "Store properly"
            ]
        }
        
        return activities.get(stage, ["Monitor crop regularly", "Follow standard practices"])
    
    def _month_names(self, month_numbers: List[int]) -> List[str]:
        """Convert month numbers to names"""
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return [months[m-1] for m in month_numbers]
    
    def get_current_stage(self, crop: str, planting_date: datetime) -> Dict:
        """Determine current growth stage based on planting date"""
        
        if crop not in self.crop_schedules:
            return {"error": f"Crop '{crop}' not found"}
        
        days_since_planting = (datetime.now() - planting_date).days
        
        if days_since_planting < 0:
            return {"stage": "Not yet planted", "days_since_planting": days_since_planting}
        
        schedule_data = self.crop_schedules[crop]
        stages = schedule_data["stages"]
        
        cumulative_days = 0
        for stage_name, duration in stages.items():
            cumulative_days += duration
            if days_since_planting < cumulative_days:
                days_in_stage = duration - (cumulative_days - days_since_planting)
                progress_percent = (days_in_stage / duration) * 100
                
                return {
                    "crop": crop,
                    "current_stage": stage_name.replace("_", " ").title(),
                    "days_since_planting": days_since_planting,
                    "days_in_current_stage": days_in_stage,
                    "stage_progress_percent": progress_percent,
                    "days_to_next_stage": duration - days_in_stage,
                    "days_to_harvest": schedule_data["total_days"] - days_since_planting,
                    "activities": self._get_stage_activities(crop, stage_name)
                }
        
        return {
            "crop": crop,
            "current_stage": "Ready for Harvest / Overdue",
            "days_since_planting": days_since_planting,
            "message": "Crop should have been harvested"
        }
    
    def recommend_planting_date(self, crop: str, location_month: int = None) -> Dict:
        """Recommend best planting dates for a crop"""
        
        if crop not in self.crop_schedules:
            return {"error": f"Crop '{crop}' not found"}
        
        if location_month is None:
            location_month = datetime.now().month
        
        schedule_data = self.crop_schedules[crop]
        best_months = schedule_data["best_sowing_months"]
        
        # Find nearest recommended month
        if location_month in best_months:
            recommendation = "Current month is ideal for planting!"
            next_planting = datetime.now()
        else:
            # Find next best month
            future_months = [m for m in best_months if m > location_month]
            if future_months:
                next_month = min(future_months)
                months_to_wait = next_month - location_month
            else:
                next_month = min(best_months)
                months_to_wait = (12 - location_month) + next_month
            
            next_planting = datetime.now() + timedelta(days=months_to_wait * 30)
            recommendation = f"Wait {months_to_wait} months for optimal planting"
        
        return {
            "crop": crop,
            "current_month": self._month_names([location_month])[0],
            "best_planting_months": self._month_names(best_months),
            "recommendation": recommendation,
            "next_planting_date": next_planting.strftime("%Y-%m-%d"),
            "total_duration": schedule_data["total_days"],
            "expected_harvest": (next_planting + timedelta(days=schedule_data["total_days"])).strftime("%Y-%m-%d")
        }
