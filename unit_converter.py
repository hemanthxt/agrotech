"""Unit conversion utilities for agricultural measurements"""

class UnitConverter:
    """Handles conversion between different agricultural units"""
    
    @staticmethod
    def area_conversion(value: float, from_unit: str, to_unit: str) -> float:
        """Convert between area units"""
        # Convert to square meters first
        to_sqm = {
            "acres": 4046.86,
            "hectares": 10000,
            "sqm": 1,
            "sqft": 0.092903,
            "bigha": 2529.29,  # Indian measurement
            "guntha": 101.17,  # Indian measurement
        }
        
        if from_unit not in to_sqm or to_unit not in to_sqm:
            return value
        
        sqm_value = value * to_sqm[from_unit]
        return sqm_value / to_sqm[to_unit]
    
    @staticmethod
    def weight_conversion(value: float, from_unit: str, to_unit: str) -> float:
        """Convert between weight units"""
        # Convert to kg first
        to_kg = {
            "kg": 1,
            "quintal": 100,
            "ton": 1000,
            "pounds": 0.453592,
            "grams": 0.001,
            "maund": 37.324,  # Indian measurement
        }
        
        if from_unit not in to_kg or to_unit not in to_kg:
            return value
        
        kg_value = value * to_kg[from_unit]
        return kg_value / to_kg[to_unit]
    
    @staticmethod
    def temperature_conversion(value: float, from_unit: str, to_unit: str) -> float:
        """Convert between temperature units"""
        if from_unit == to_unit:
            return value
        
        # Convert to Celsius first
        if from_unit == "fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "kelvin":
            celsius = value - 273.15
        else:
            celsius = value
        
        # Convert from Celsius to target
        if to_unit == "fahrenheit":
            return (celsius * 9/5) + 32
        elif to_unit == "kelvin":
            return celsius + 273.15
        else:
            return celsius
    
    @staticmethod
    def volume_conversion(value: float, from_unit: str, to_unit: str) -> float:
        """Convert between volume units (for irrigation)"""
        # Convert to liters first
        to_liters = {
            "liters": 1,
            "cubic_meters": 1000,
            "gallons": 3.78541,
            "cubic_feet": 28.3168,
        }
        
        if from_unit not in to_liters or to_unit not in to_liters:
            return value
        
        liters_value = value * to_liters[from_unit]
        return liters_value / to_liters[to_unit]
    
    @staticmethod
    def format_area(value: float, unit: str) -> str:
        """Format area with appropriate unit symbol"""
        symbols = {
            "acres": "ac",
            "hectares": "ha",
            "sqm": "m²",
            "sqft": "ft²",
            "bigha": "bigha",
            "guntha": "guntha",
        }
        return f"{value:.2f} {symbols.get(unit, unit)}"
    
    @staticmethod
    def format_weight(value: float, unit: str) -> str:
        """Format weight with appropriate unit symbol"""
        symbols = {
            "kg": "kg",
            "quintal": "q",
            "ton": "t",
            "pounds": "lbs",
            "grams": "g",
            "maund": "maund",
        }
        return f"{value:.2f} {symbols.get(unit, unit)}"
