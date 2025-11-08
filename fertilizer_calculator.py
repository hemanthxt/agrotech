"""Fertilizer calculation and NPK recommendations"""
from typing import Dict, List

class FertilizerCalculator:
    """Calculate fertilizer requirements and NPK ratios"""
    
    def __init__(self):
        # NPK requirements for crops (kg per acre)
        self.crop_npk_requirements = {
            "Wheat": {"N": 60, "P": 30, "K": 20},
            "Rice": {"N": 80, "P": 40, "K": 40},
            "Corn": {"N": 75, "P": 35, "K": 30},
            "Cotton": {"N": 90, "P": 45, "K": 45},
            "Soybeans": {"N": 20, "P": 40, "K": 30},  # Low N due to fixation
            "Sugarcane": {"N": 120, "P": 60, "K": 60},
            "Potatoes": {"N": 70, "P": 50, "K": 80},
            "Tomatoes": {"N": 80, "P": 60, "K": 100},
            "Onions": {"N": 60, "P": 30, "K": 60},
            "Cabbage": {"N": 75, "P": 40, "K": 50},
            "Groundnut": {"N": 15, "P": 40, "K": 30},
            "Chickpea": {"N": 15, "P": 30, "K": 20},
        }
        
        # Common fertilizers and their nutrient content (%)
        self.fertilizer_types = {
            "Urea": {"N": 46, "P": 0, "K": 0, "price_per_kg": 6},
            "DAP": {"N": 18, "P": 46, "K": 0, "price_per_kg": 27},
            "MOP": {"N": 0, "P": 0, "K": 60, "price_per_kg": 17},
            "NPK_10_26_26": {"N": 10, "P": 26, "K": 26, "price_per_kg": 25},
            "NPK_19_19_19": {"N": 19, "P": 19, "K": 19, "price_per_kg": 28},
            "SSP": {"N": 0, "P": 16, "K": 0, "price_per_kg": 8},
            "Ammonium_Sulphate": {"N": 21, "P": 0, "K": 0, "price_per_kg": 9},
        }
        
        # Organic fertilizers
        self.organic_fertilizers = {
            "Cow_Manure": {"N": 0.5, "P": 0.3, "K": 0.5, "application_ton_per_acre": 5},
            "Compost": {"N": 1.0, "P": 0.5, "K": 0.5, "application_ton_per_acre": 3},
            "Poultry_Manure": {"N": 3.0, "P": 2.0, "K": 1.5, "application_ton_per_acre": 2},
            "Vermicompost": {"N": 2.0, "P": 1.5, "K": 1.0, "application_ton_per_acre": 2},
            "Green_Manure": {"N": 0.4, "P": 0.2, "K": 0.3, "application_ton_per_acre": 10},
        }
    
    def calculate_fertilizer_requirement(self, crop: str, area_acres: float, 
                                        soil_test: Dict = None) -> Dict:
        """Calculate fertilizer requirements for a crop"""
        
        if crop not in self.crop_npk_requirements:
            # Default NPK for unknown crops
            base_npk = {"N": 60, "P": 40, "K": 40}
        else:
            base_npk = self.crop_npk_requirements[crop]
        
        # Adjust based on soil test if provided
        if soil_test:
            n_needed = max(0, base_npk["N"] - soil_test.get("N", 0))
            p_needed = max(0, base_npk["P"] - soil_test.get("P", 0))
            k_needed = max(0, base_npk["K"] - soil_test.get("K", 0))
        else:
            # Assume 70% of requirement needed (some nutrients already in soil)
            n_needed = base_npk["N"] * 0.7
            p_needed = base_npk["P"] * 0.7
            k_needed = base_npk["K"] * 0.7
        
        # Total requirement for the area
        total_n = n_needed * area_acres
        total_p = p_needed * area_acres
        total_k = k_needed * area_acres
        
        return {
            "crop": crop,
            "area_acres": area_acres,
            "npk_per_acre": {"N": n_needed, "P": p_needed, "K": k_needed},
            "total_npk_required": {"N": total_n, "P": total_p, "K": total_k},
            "base_requirement": base_npk,
            "soil_tested": soil_test is not None
        }
    
    def recommend_fertilizers(self, npk_required: Dict, area_acres: float, 
                             prefer_organic: bool = False) -> Dict:
        """Recommend specific fertilizers to meet NPK requirements"""
        
        n_req = npk_required["N"]
        p_req = npk_required["P"]
        k_req = npk_required["K"]
        
        if prefer_organic:
            return self._organic_fertilizer_plan(n_req, p_req, k_req, area_acres)
        
        # Chemical fertilizer recommendation
        # Strategy: Use DAP for P, MOP for K, Urea for remaining N
        
        # Step 1: DAP for phosphorus
        dap_needed = p_req / (self.fertilizer_types["DAP"]["P"] / 100)
        n_from_dap = dap_needed * (self.fertilizer_types["DAP"]["N"] / 100)
        
        # Step 2: MOP for potassium
        mop_needed = k_req / (self.fertilizer_types["MOP"]["K"] / 100)
        
        # Step 3: Urea for remaining nitrogen
        remaining_n = max(0, n_req - n_from_dap)
        urea_needed = remaining_n / (self.fertilizer_types["Urea"]["N"] / 100)
        
        # Calculate costs
        dap_cost = dap_needed * self.fertilizer_types["DAP"]["price_per_kg"]
        mop_cost = mop_needed * self.fertilizer_types["MOP"]["price_per_kg"]
        urea_cost = urea_needed * self.fertilizer_types["Urea"]["price_per_kg"]
        total_cost = dap_cost + mop_cost + urea_cost
        
        fertilizer_plan = [
            {
                "fertilizer": "Urea",
                "quantity_kg": round(urea_needed, 2),
                "cost": round(urea_cost, 2),
                "application": "Split: 50% at sowing, 25% at 30 days, 25% at 60 days"
            },
            {
                "fertilizer": "DAP",
                "quantity_kg": round(dap_needed, 2),
                "cost": round(dap_cost, 2),
                "application": "Apply at sowing time"
            },
            {
                "fertilizer": "MOP (Potash)",
                "quantity_kg": round(mop_needed, 2),
                "cost": round(mop_cost, 2),
                "application": "Apply at sowing or early vegetative stage"
            }
        ]
        
        return {
            "fertilizer_plan": fertilizer_plan,
            "total_cost": round(total_cost, 2),
            "cost_per_acre": round(total_cost / area_acres, 2) if area_acres > 0 else 0,
            "npk_provided": npk_required,
            "type": "chemical"
        }
    
    def _organic_fertilizer_plan(self, n_req: float, p_req: float, 
                                k_req: float, area_acres: float) -> Dict:
        """Create organic fertilizer plan"""
        
        # Use compost as base
        compost_tons = area_acres * 3  # 3 tons per acre
        n_from_compost = compost_tons * 1000 * (self.organic_fertilizers["Compost"]["N"] / 100)
        p_from_compost = compost_tons * 1000 * (self.organic_fertilizers["Compost"]["P"] / 100)
        k_from_compost = compost_tons * 1000 * (self.organic_fertilizers["Compost"]["K"] / 100)
        
        # Additional poultry manure if needed
        remaining_n = max(0, n_req - n_from_compost)
        poultry_tons = 0
        if remaining_n > 0:
            poultry_tons = min(area_acres * 2, remaining_n / (self.organic_fertilizers["Poultry_Manure"]["N"] * 10))
        
        fertilizer_plan = [
            {
                "fertilizer": "Compost",
                "quantity_tons": round(compost_tons, 2),
                "cost": round(compost_tons * 2000, 2),  # ₹2000 per ton
                "application": "Apply 2-3 weeks before sowing, mix with soil"
            }
        ]
        
        if poultry_tons > 0:
            fertilizer_plan.append({
                "fertilizer": "Poultry Manure",
                "quantity_tons": round(poultry_tons, 2),
                "cost": round(poultry_tons * 3000, 2),  # ₹3000 per ton
                "application": "Apply well-composted manure before sowing"
            })
        
        total_cost = sum(item["cost"] for item in fertilizer_plan)
        
        return {
            "fertilizer_plan": fertilizer_plan,
            "total_cost": round(total_cost, 2),
            "cost_per_acre": round(total_cost / area_acres, 2) if area_acres > 0 else 0,
            "npk_provided": {
                "N": n_from_compost + (poultry_tons * 1000 * 0.03 if poultry_tons > 0 else 0),
                "P": p_from_compost,
                "K": k_from_compost
            },
            "type": "organic",
            "benefits": [
                "Improves soil structure",
                "Increases water retention",
                "Adds beneficial microorganisms",
                "Slow-release nutrients"
            ]
        }
    
    def split_application_schedule(self, crop: str, fertilizer_plan: List[Dict]) -> List[Dict]:
        """Create a time-based fertilizer application schedule"""
        
        # General splitting strategy for cereals
        schedule = [
            {
                "stage": "Basal (At Sowing)",
                "days_after_sowing": 0,
                "fertilizers": [],
                "notes": "Apply before or during sowing"
            },
            {
                "stage": "First Top Dressing",
                "days_after_sowing": 30,
                "fertilizers": [],
                "notes": "Apply after first irrigation"
            },
            {
                "stage": "Second Top Dressing",
                "days_after_sowing": 60,
                "fertilizers": [],
                "notes": "Apply before flowering"
            }
        ]
        
        for fert in fertilizer_plan:
            fert_name = fert["fertilizer"]
            quantity = fert["quantity_kg"]
            
            if "DAP" in fert_name or "MOP" in fert_name or "SSP" in fert_name:
                # Full phosphorus and potassium at sowing
                schedule[0]["fertilizers"].append({
                    "name": fert_name,
                    "quantity_kg": quantity
                })
            elif "Urea" in fert_name or "Ammonium" in fert_name:
                # Split nitrogen application
                schedule[0]["fertilizers"].append({
                    "name": fert_name,
                    "quantity_kg": round(quantity * 0.5, 2)
                })
                schedule[1]["fertilizers"].append({
                    "name": fert_name,
                    "quantity_kg": round(quantity * 0.25, 2)
                })
                schedule[2]["fertilizers"].append({
                    "name": fert_name,
                    "quantity_kg": round(quantity * 0.25, 2)
                })
        
        return schedule
    
    def micronutrient_recommendations(self, crop: str, symptoms: List[str] = None) -> Dict:
        """Recommend micronutrient applications"""
        
        micronutrients = {
            "Zinc": {
                "crops_needing": ["Rice", "Corn", "Wheat"],
                "symptoms": ["yellowing between veins", "stunted growth"],
                "application": "Apply 25 kg Zinc Sulphate per acre",
                "cost_per_acre": 500
            },
            "Iron": {
                "crops_needing": ["Groundnut", "Chickpea", "Citrus"],
                "symptoms": ["yellowing of young leaves", "interveinal chlorosis"],
                "application": "Foliar spray of Ferrous Sulphate 0.5%",
                "cost_per_acre": 300
            },
            "Boron": {
                "crops_needing": ["Cotton", "Sunflower", "Groundnut"],
                "symptoms": ["hollow stems", "flower drop", "poor seed set"],
                "application": "Apply 10 kg Borax per acre",
                "cost_per_acre": 400
            },
            "Manganese": {
                "crops_needing": ["Soybeans", "Wheat", "Oats"],
                "symptoms": ["interveinal chlorosis", "gray speck"],
                "application": "Foliar spray of Manganese Sulphate 0.5%",
                "cost_per_acre": 250
            }
        }
        
        recommendations = []
        
        for nutrient, info in micronutrients.items():
            if crop in info["crops_needing"]:
                recommendations.append({
                    "nutrient": nutrient,
                    "application": info["application"],
                    "cost_per_acre": info["cost_per_acre"],
                    "priority": "High" if symptoms and any(s in symptoms for s in info["symptoms"]) else "Medium"
                })
        
        return {
            "crop": crop,
            "recommendations": recommendations,
            "total_cost": sum(r["cost_per_acre"] for r in recommendations)
        }
