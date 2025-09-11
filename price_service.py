import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st
import numpy as np

class PriceService:
    """Service for fetching agricultural commodity prices and predictions"""
    
    def __init__(self):
        # Using free APIs for commodity prices
        self.commodities_api_base = "https://api.api-ninjas.com/v1/commodityprice"
        self.api_key = None  # Will use free endpoints initially
        
        # Crop to commodity mapping
        self.crop_commodity_map = {
            "Wheat": "wheat",
            "Corn": "corn", 
            "Rice": "rice",
            "Soybeans": "soybeans",
            "Cotton": "cotton",
            "Tomatoes": "tomatoes",
            "Potatoes": "potatoes",
            "Lettuce": "lettuce",
            "Carrots": "carrots",
            "Onions": "onions",
            "Cucumbers": "cucumbers",
            "Peppers": "peppers",
            "Spinach": "spinach",
            "Broccoli": "broccoli",
            "Cabbage": "cabbage",
            "Beans": "beans",
            "Peas": "peas",
            "Squash": "squash",
            "Eggplant": "eggplant",
            "Radishes": "radishes",
            "Cauliflower": "cauliflower",
            "Okra": "okra",
            "Beetroot": "beetroot",
            "Turnip": "turnip",
            "Ginger": "ginger",
            "Garlic": "garlic",
            "Coriander": "coriander",
            "Mint": "mint",
            "Fenugreek": "fenugreek",
            "Mustard": "mustard",
            "Green Chili": "green_chili",
            "Turmeric": "turmeric",
            "Sugarcane": "sugarcane",
            "Banana": "banana",
            "Mango": "mango",
            "Apple": "apple",
            "Grapes": "grapes",
            "Orange": "orange",
            "Coconut": "coconut",
            "Cashew": "cashew",
            "Groundnut": "groundnut",
            "Sesame": "sesame",
            "Sunflower": "sunflower",
            "Safflower": "safflower",
            "Castor": "castor",
            "Marigold": "marigold",
            "Rose": "rose"
        }
        
        # Mock historical data for demonstration (in real implementation, this would come from APIs)
        # Prices in Indian Rupees (INR) per kilogram
        self.mock_prices = {
            "wheat": {"current": 20.84, "unit": "INR/kg", "change": 2.3},
            "corn": {"current": 15.0, "unit": "INR/kg", "change": -1.2},
            "rice": {"current": 35.0, "unit": "INR/kg", "change": 5.1},
            "soybeans": {"current": 43.3, "unit": "INR/kg", "change": 3.8},
            "cotton": {"current": 154.0, "unit": "INR/kg", "change": -2.5},
            "tomatoes": {"current": 99.8, "unit": "INR/kg", "change": 4.2},
            "potatoes": {"current": 29.15, "unit": "INR/kg", "change": 1.8},
            "lettuce": {"current": 66.5, "unit": "INR/kg", "change": 6.5},
            "carrots": {"current": 37.45, "unit": "INR/kg", "change": -0.8},
            "onions": {"current": 31.62, "unit": "INR/kg", "change": 2.1},
            "cucumbers": {"current": 76.55, "unit": "INR/kg", "change": 3.2},
            "peppers": {"current": 120.75, "unit": "INR/kg", "change": 1.8},
            "spinach": {"current": 108.25, "unit": "INR/kg", "change": 4.5},
            "broccoli": {"current": 62.45, "unit": "INR/kg", "change": 2.1},
            "cabbage": {"current": 39.95, "unit": "INR/kg", "change": -1.3},
            "beans": {"current": 95.75, "unit": "INR/kg", "change": 3.7},
            "peas": {"current": 87.45, "unit": "INR/kg", "change": 2.9},
            "squash": {"current": 56.65, "unit": "INR/kg", "change": 1.4},
            "eggplant": {"current": 91.65, "unit": "INR/kg", "change": 2.6},
            "radishes": {"current": 43.3, "unit": "INR/kg", "change": 1.9},
            "cauliflower": {"current": 48.5, "unit": "INR/kg", "change": 2.8},
            "okra": {"current": 85.2, "unit": "INR/kg", "change": 3.1},
            "beetroot": {"current": 52.4, "unit": "INR/kg", "change": 1.6},
            "turnip": {"current": 28.9, "unit": "INR/kg", "change": -0.5},
            "ginger": {"current": 245.8, "unit": "INR/kg", "change": 4.7},
            "garlic": {"current": 189.3, "unit": "INR/kg", "change": 2.2},
            "coriander": {"current": 125.6, "unit": "INR/kg", "change": 6.3},
            "mint": {"current": 98.7, "unit": "INR/kg", "change": 3.9},
            "fenugreek": {"current": 78.4, "unit": "INR/kg", "change": 1.8},
            "mustard": {"current": 65.2, "unit": "INR/kg", "change": 2.1},
            "green_chili": {"current": 158.3, "unit": "INR/kg", "change": 4.8},
            "turmeric": {"current": 210.5, "unit": "INR/kg", "change": 3.2},
            "sugarcane": {"current": 3.5, "unit": "INR/kg", "change": 1.1},
            "banana": {"current": 45.8, "unit": "INR/kg", "change": 2.7},
            "mango": {"current": 85.4, "unit": "INR/kg", "change": 3.6},
            "apple": {"current": 165.2, "unit": "INR/kg", "change": 1.9},
            "grapes": {"current": 125.8, "unit": "INR/kg", "change": 2.4},
            "orange": {"current": 68.9, "unit": "INR/kg", "change": 1.7},
            "coconut": {"current": 35.6, "unit": "INR/kg", "change": 2.8},
            "cashew": {"current": 850.0, "unit": "INR/kg", "change": 4.2},
            "groundnut": {"current": 98.5, "unit": "INR/kg", "change": 3.1},
            "sesame": {"current": 142.7, "unit": "INR/kg", "change": 2.9},
            "sunflower": {"current": 78.3, "unit": "INR/kg", "change": 1.8},
            "safflower": {"current": 89.2, "unit": "INR/kg", "change": 2.6},
            "castor": {"current": 67.4, "unit": "INR/kg", "change": 1.4},
            "marigold": {"current": 45.8, "unit": "INR/kg", "change": 3.2},
            "rose": {"current": 120.5, "unit": "INR/kg", "change": 2.8}
        }
    
    @st.cache_data(ttl=1800)  # Cache for 30 minutes
    def get_current_price(_self, crop_type: str) -> Optional[Dict]:
        """Get current market price for a crop"""
        try:
            commodity = _self.crop_commodity_map.get(crop_type)
            if not commodity:
                return None
            
            # For now, using mock data - in production, this would call real APIs
            if commodity in _self.mock_prices:
                price_data = _self.mock_prices[commodity].copy()
                price_data['commodity'] = commodity
                price_data['timestamp'] = datetime.now().isoformat()
                price_data['crop_type'] = crop_type
                return price_data
            
            return None
            
        except Exception as e:
            st.error(f"Error fetching price data: {str(e)}")
            return None
    
    def generate_historical_data(self, crop_type: str, days: int = 30) -> Optional[pd.DataFrame]:
        """Generate mock historical price data for demonstration"""
        try:
            commodity = self.crop_commodity_map.get(crop_type)
            if not commodity or commodity not in self.mock_prices:
                return None
            
            base_price = self.mock_prices[commodity]["current"]
            dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
            
            # Generate realistic price variations
            np.random.seed(42)  # For consistent results
            price_variations = np.random.normal(0, base_price * 0.02, days)  # 2% volatility
            prices = []
            
            current_price = base_price * 0.95  # Start slightly lower
            for i, variation in enumerate(price_variations):
                current_price += variation
                # Add some trend and seasonality
                trend = (i / days) * base_price * 0.05  # Slight upward trend
                seasonal = np.sin(i / 7) * base_price * 0.01  # Weekly pattern
                final_price = max(current_price + trend + seasonal, base_price * 0.7)
                prices.append(final_price)
            
            df = pd.DataFrame({
                'Date': dates,
                'Price': prices,
                'Crop': crop_type
            })
            
            return df
            
        except Exception as e:
            st.error(f"Error generating historical data: {str(e)}")
            return None
    
    def predict_future_prices(self, crop_type: str, days: int = 7) -> Optional[pd.DataFrame]:
        """Simple price prediction based on trends"""
        try:
            historical_data = self.generate_historical_data(crop_type, 30)
            if historical_data is None:
                return None
            
            # Simple moving average prediction
            recent_prices = historical_data['Price'].tail(7).values
            avg_daily_change = np.mean(np.diff(recent_prices))
            
            future_dates = [datetime.now() + timedelta(days=i+1) for i in range(days)]
            current_price = recent_prices[-1]
            
            predicted_prices = []
            for i in range(days):
                # Add some randomness to predictions
                trend_component = avg_daily_change * (i + 1)
                random_component = np.random.normal(0, current_price * 0.01)
                predicted_price = current_price + trend_component + random_component
                predicted_prices.append(max(predicted_price, current_price * 0.8))
            
            prediction_df = pd.DataFrame({
                'Date': future_dates,
                'Predicted_Price': predicted_prices,
                'Crop': crop_type,
                'Confidence': np.random.uniform(0.7, 0.9, days)  # Mock confidence scores
            })
            
            return prediction_df
            
        except Exception as e:
            st.error(f"Error predicting prices: {str(e)}")
            return None
    
    def get_market_analysis(self, crop_type: str) -> Dict:
        """Provide market analysis and recommendations"""
        current_price = self.get_current_price(crop_type)
        historical_data = self.generate_historical_data(crop_type, 30)
        
        if not current_price or historical_data is None:
            return {"status": "error", "message": "Unable to analyze market data"}
        
        # Calculate market indicators
        avg_30_day = historical_data['Price'].mean()
        current_vs_avg = ((current_price['current'] - avg_30_day) / avg_30_day) * 100
        
        # Price volatility
        price_std = historical_data['Price'].std()
        volatility = (price_std / avg_30_day) * 100
        
        # Trend analysis
        recent_trend = np.polyfit(range(7), historical_data['Price'].tail(7).values, 1)[0]
        
        # Generate recommendations
        recommendations = []
        
        if current_vs_avg > 5:
            recommendations.append("🟢 Prices are above 30-day average - good time to sell")
        elif current_vs_avg < -5:
            recommendations.append("🔴 Prices are below 30-day average - consider holding")
        else:
            recommendations.append("🟡 Prices are near average - monitor market conditions")
        
        if recent_trend > 0:
            recommendations.append("📈 Recent trend is upward - prices may continue rising")
        elif recent_trend < 0:
            recommendations.append("📉 Recent trend is downward - prices may continue falling")
        else:
            recommendations.append("➡️ Recent trend is stable - consistent pricing expected")
        
        if volatility > 10:
            recommendations.append("⚡ High volatility detected - expect price swings")
        else:
            recommendations.append("🔄 Low volatility - stable price environment")
        
        return {
            "status": "success",
            "current_price": current_price['current'],
            "currency": "INR/kg",
            "change_percent": current_price['change'],
            "vs_30day_avg": current_vs_avg,
            "volatility": volatility,
            "trend": "upward" if recent_trend > 0 else "downward" if recent_trend < 0 else "stable",
            "recommendations": recommendations
        }
    
    def get_best_selling_time(self, crop_type: str) -> Dict:
        """Recommend optimal selling time based on predictions"""
        predictions = self.predict_future_prices(crop_type, 30)
        current_price = self.get_current_price(crop_type)
        
        if predictions is None or not current_price:
            return {"status": "error", "message": "Unable to determine optimal selling time"}
        
        # Find the best price in predictions
        best_price_idx = predictions['Predicted_Price'].idxmax()
        best_price = predictions.loc[best_price_idx, 'Predicted_Price']
        best_date = predictions.loc[best_price_idx, 'Date']
        
        days_to_best = (best_date - datetime.now()).days
        price_increase = ((best_price - current_price['current']) / current_price['current']) * 100
        
        if days_to_best <= 3 and price_increase > 2:
            recommendation = f"🚀 Sell in {days_to_best} days for {price_increase:.1f}% higher price"
            action = "wait"
        elif days_to_best > 7 and price_increase > 5:
            recommendation = f"💰 Consider waiting {days_to_best} days for {price_increase:.1f}% price increase"
            action = "hold"
        elif price_increase < 1:
            recommendation = "💸 Current prices are near optimal - consider selling soon"
            action = "sell_now"
        else:
            recommendation = f"📊 Monitor market - potential {price_increase:.1f}% gain in {days_to_best} days"
            action = "monitor"
        
        return {
            "status": "success",
            "recommendation": recommendation,
            "action": action,
            "optimal_date": best_date.strftime("%Y-%m-%d"),
            "days_to_wait": days_to_best,
            "expected_price": best_price,
            "potential_gain_percent": price_increase
        }