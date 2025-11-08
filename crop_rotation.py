"""Crop rotation planning for sustainable farming"""
from typing import Dict, List

class CropRotationPlanner:
    """Plan crop rotations for soil health and pest management"""
    
    def __init__(self):
        # Crop families for rotation planning
        self.crop_families = {
            "legumes": ["Soybeans", "Peas", "Beans", "Groundnut", "Chickpea", "Lentils"],
            "cereals": ["Wheat", "Rice", "Corn", "Barley", "Oats", "Sorghum", "Millet"],
            "brassicas": ["Cabbage", "Cauliflower", "Broccoli", "Mustard", "Radish", "Turnip"],
            "solanaceae": ["Tomatoes", "Potatoes", "Peppers", "Eggplant"],
            "cucurbits": ["Cucumbers", "Pumpkin", "Squash", "Watermelon", "Muskmelon"],
            "alliums": ["Onions", "Garlic", "Leek"],
            "root_vegetables": ["Carrots", "Beetroot", "Radishes"],
            "leafy_greens": ["Spinach", "Lettuce", "Cabbage", "Kale"],
        }
        
        # Nitrogen requirements (high/medium/low)
        self.nitrogen_needs = {
            "high": ["Corn", "Cabbage", "Spinach", "Lettuce", "Rice", "Sugarcane"],
            "medium": ["Wheat", "Tomatoes", "Peppers", "Cucumbers", "Onions", "Cotton"],
            "low": ["Carrots", "Potatoes", "Radishes", "Beetroot"],
            "fixing": ["Soybeans", "Peas", "Beans", "Groundnut", "Chickpea", "Lentils"]  # Nitrogen fixers
        }
        
        # Pest and disease vulnerabilities
        self.pest_concerns = {
            "Wheat": ["rust", "aphids", "stem_borer"],
            "Rice": ["blast", "stem_borer", "brown_planthopper"],
            "Corn": ["corn_borer", "fall_armyworm", "rust"],
            "Soybeans": ["pod_borer", "rust", "leaf_spot"],
            "Cotton": ["bollworm", "whitefly", "aphids"],
            "Tomatoes": ["blight", "whitefly", "fruit_borer"],
            "Potatoes": ["blight", "aphids", "beetle"],
        }
    
    def suggest_rotation(self, current_crop: str, years: int = 3) -> Dict:
        """Suggest crop rotation sequence"""
        
        # Find current crop family
        current_family = self._find_crop_family(current_crop)
        current_n_need = self._find_nitrogen_category(current_crop)
        
        # Rotation principles:
        # 1. Don't repeat same family consecutively
        # 2. Follow high N feeder with legume or low N feeder
        # 3. Alternate root depth
        # 4. Break pest cycles
        
        rotation_sequence = [current_crop]
        
        # Year 2: Complement current crop
        if current_n_need == "high":
            # Follow with legume or low feeder
            candidates = self.nitrogen_needs["fixing"] + self.nitrogen_needs["low"]
        elif current_n_need == "fixing":
            # Follow with high feeder to use fixed nitrogen
            candidates = self.nitrogen_needs["high"]
        else:
            # Medium or low - can follow with legume
            candidates = self.nitrogen_needs["fixing"]
        
        # Remove crops from same family
        candidates = [c for c in candidates if self._find_crop_family(c) != current_family]
        
        if candidates:
            year2_crop = candidates[0]
            rotation_sequence.append(year2_crop)
        else:
            year2_crop = "Wheat"  # Default safe option
            rotation_sequence.append(year2_crop)
        
        # Year 3: Different family again
        year2_family = self._find_crop_family(year2_crop)
        candidates = []
        for family, crops in self.crop_families.items():
            if family != current_family and family != year2_family:
                candidates.extend(crops)
        
        if len(candidates) > 0:
            year3_crop = candidates[0]
        else:
            year3_crop = "Corn"
        
        rotation_sequence.append(year3_crop)
        
        # Additional years if requested
        while len(rotation_sequence) < years:
            rotation_sequence.append(rotation_sequence[0])  # Cycle back
        
        # Generate detailed plan
        rotation_plan = []
        for i, crop in enumerate(rotation_sequence[:years]):
            rotation_plan.append({
                "year": i + 1,
                "crop": crop,
                "family": self._find_crop_family(crop),
                "nitrogen_need": self._find_nitrogen_category(crop),
                "benefits": self._get_rotation_benefits(crop, i, rotation_sequence)
            })
        
        return {
            "current_crop": current_crop,
            "rotation_sequence": rotation_sequence[:years],
            "rotation_plan": rotation_plan,
            "overall_benefits": self._calculate_overall_benefits(rotation_sequence[:years])
        }
    
    def _find_crop_family(self, crop: str) -> str:
        """Find which family a crop belongs to"""
        for family, crops in self.crop_families.items():
            if crop in crops:
                return family
        return "other"
    
    def _find_nitrogen_category(self, crop: str) -> str:
        """Find nitrogen requirement category"""
        for category, crops in self.nitrogen_needs.items():
            if crop in crops:
                return category
        return "medium"
    
    def _get_rotation_benefits(self, crop: str, year_index: int, sequence: List[str]) -> List[str]:
        """List benefits of this crop in the rotation"""
        benefits = []
        
        n_category = self._find_nitrogen_category(crop)
        
        if n_category == "fixing":
            benefits.append("Adds nitrogen to soil naturally")
            benefits.append("Improves soil structure")
        
        if year_index > 0:
            prev_crop = sequence[year_index - 1]
            prev_family = self._find_crop_family(prev_crop)
            curr_family = self._find_crop_family(crop)
            
            if prev_family != curr_family:
                benefits.append("Breaks pest and disease cycles")
            
            prev_n = self._find_nitrogen_category(prev_crop)
            if prev_n == "fixing" and n_category == "high":
                benefits.append("Utilizes nitrogen fixed by previous crop")
        
        if n_category == "low":
            benefits.append("Allows soil nitrogen recovery")
        
        return benefits if benefits else ["Maintains crop diversity"]
    
    def _calculate_overall_benefits(self, sequence: List[str]) -> List[str]:
        """Calculate cumulative benefits of the rotation plan"""
        benefits = []
        
        families = [self._find_crop_family(c) for c in sequence]
        if len(set(families)) == len(families):
            benefits.append("✅ Excellent family diversity - minimizes pest buildup")
        elif len(set(families)) > 1:
            benefits.append("✅ Good crop diversity")
        
        has_legume = any(self._find_nitrogen_category(c) == "fixing" for c in sequence)
        if has_legume:
            benefits.append("✅ Includes nitrogen-fixing crops - reduces fertilizer needs")
        
        n_categories = [self._find_nitrogen_category(c) for c in sequence]
        if "high" in n_categories and "fixing" in n_categories:
            benefits.append("✅ Balanced nitrogen management")
        
        benefits.append("✅ Improves soil health and sustainability")
        benefits.append("✅ Reduces dependency on chemical inputs")
        
        return benefits
    
    def check_compatibility(self, crop1: str, crop2: str) -> Dict:
        """Check if two crops are compatible for succession"""
        
        family1 = self._find_crop_family(crop1)
        family2 = self._find_crop_family(crop2)
        
        n1 = self._find_nitrogen_category(crop1)
        n2 = self._find_nitrogen_category(crop2)
        
        compatibility_score = 0
        reasons = []
        
        # Family diversity
        if family1 != family2:
            compatibility_score += 30
            reasons.append("✅ Different plant families - good for pest management")
        else:
            reasons.append("⚠️ Same family - may increase pest/disease risk")
        
        # Nitrogen balance
        if n1 == "fixing" and n2 == "high":
            compatibility_score += 40
            reasons.append("✅ Excellent nitrogen balance - legume followed by heavy feeder")
        elif n1 == "high" and n2 == "fixing":
            compatibility_score += 30
            reasons.append("✅ Good nitrogen recovery strategy")
        elif n1 == "high" and n2 == "high":
            compatibility_score -= 20
            reasons.append("⚠️ Both are heavy feeders - will deplete soil")
        else:
            compatibility_score += 10
            reasons.append("✓ Acceptable nitrogen balance")
        
        # Overall assessment
        if compatibility_score >= 50:
            recommendation = "Highly Recommended"
            color = "green"
        elif compatibility_score >= 20:
            recommendation = "Acceptable"
            color = "yellow"
        else:
            recommendation = "Not Recommended"
            color = "red"
        
        return {
            "crop1": crop1,
            "crop2": crop2,
            "compatibility_score": max(0, min(100, compatibility_score + 30)),  # Normalize to 0-100
            "recommendation": recommendation,
            "reasons": reasons,
            "color": color
        }
