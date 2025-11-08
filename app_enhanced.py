"""
Enhanced Agricultural Assistant with Advanced Features
Includes: Dark Mode, Export Data, Multi-crop Comparison, Financial Tools, 
Irrigation Calculator, Farm Calendar, Crop Rotation, Fertilizer Calculator
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json

from weather_service import WeatherService
from crop_recommendations import CropRecommendations
from price_service import PriceService
from utils import format_temperature, format_precipitation, get_weather_icon
from unit_converter import UnitConverter
from financial_calculator import FinancialCalculator
from irrigation_calculator import IrrigationCalculator
from farm_calendar import FarmCalendar
from crop_rotation import CropRotationPlanner
from fertilizer_calculator import FertilizerCalculator

# Page configuration
st.set_page_config(
    page_title="Agricultural Assistant Pro",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Dark mode toggle
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply theme and mobile optimization
mobile_css = """
<style>
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        .stButton button {
            width: 100%;
            font-size: 16px;
            padding: 0.75rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .stDataFrame {
            font-size: 12px;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h2 {
            font-size: 1.2rem !important;
        }
        h3 {
            font-size: 1rem !important;
        }
    }
    
    /* Touch-friendly buttons */
    .stButton button {
        min-height: 44px;
        border-radius: 8px;
    }
    
    /* Better number inputs on mobile */
    input[type="number"] {
        font-size: 16px !important;
    }
</style>
"""

if st.session_state.dark_mode:
    st.markdown(mobile_css + """
    <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2D2D2D;
        }
        .stTabs [data-baseweb="tab"] {
            color: #FFFFFF;
        }
        .stMetric {
            background-color: #2D2D2D !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(mobile_css, unsafe_allow_html=True)

# Initialize services
@st.cache_resource
def init_services():
    weather_service = WeatherService()
    crop_recommendations = CropRecommendations()
    price_service = PriceService()
    unit_converter = UnitConverter()
    financial_calc = FinancialCalculator()
    irrigation_calc = IrrigationCalculator()
    farm_calendar = FarmCalendar()
    rotation_planner = CropRotationPlanner()
    fertilizer_calc = FertilizerCalculator()
    return (weather_service, crop_recommendations, price_service, unit_converter,
            financial_calc, irrigation_calc, farm_calendar, rotation_planner, fertilizer_calc)

(weather_service, crop_recommendations, price_service, unit_converter,
 financial_calc, irrigation_calc, farm_calendar, rotation_planner, fertilizer_calc) = init_services()

# Main header
col1, col2 = st.columns([6, 1])
with col1:
    st.title("🌾 Agricultural Assistant Pro")
    st.markdown("Complete farming solution with advanced planning tools")
with col2:
    theme_button = st.button("🌓 Theme", on_click=toggle_theme)

# Sidebar
st.sidebar.header("🌍 Farm Location")

# Location input methods
location_method = st.sidebar.radio(
    "How would you like to set your location?",
    ["🔍 Search by Place Name", "🌐 Auto-Detect Current Location", "📍 Enter Coordinates Manually"],
    index=0
)

# Initialize session state variables
if 'selected_latitude' not in st.session_state:
    st.session_state.selected_latitude = 28.6139
if 'selected_longitude' not in st.session_state:
    st.session_state.selected_longitude = 77.2090
if 'selected_location_name' not in st.session_state:
    st.session_state.selected_location_name = "New Delhi, Delhi, India"

# Method 1: Search by Place Name
if location_method == "🔍 Search by Place Name":
    st.sidebar.subheader("🔍 Search for Your Location")
    
    search_query = st.sidebar.text_input(
        "Type a place name",
        placeholder="e.g., Mumbai, Maharashtra, India",
        help="Start typing to search for cities, towns, or regions"
    )
    
    if search_query and len(search_query) >= 2:
        with st.spinner("🔍 Searching locations..."):
            search_results = weather_service.search_locations(search_query)
            
            if search_results:
                st.sidebar.success(f"✅ Found {len(search_results)} locations")
                
                location_options = [f"{loc['name']} ({loc['latitude']:.4f}, {loc['longitude']:.4f})" for loc in search_results]
                selected_idx = st.sidebar.selectbox(
                    "Select your location:",
                    range(len(location_options)),
                    format_func=lambda x: location_options[x],
                    help="Choose the most accurate match for your location"
                )
                
                if st.sidebar.button("📍 Use This Location", type="primary"):
                    selected_location = search_results[selected_idx]
                    st.session_state.selected_latitude = selected_location['latitude']
                    st.session_state.selected_longitude = selected_location['longitude']
                    st.session_state.selected_location_name = selected_location['name']
                    st.sidebar.success(f"✅ Location set to: **{selected_location['name']}**")
                    st.rerun()
            else:
                st.sidebar.warning("❌ No locations found. Try a different search term.")

# Method 2: Auto-detect current location
elif location_method == "🌐 Auto-Detect Current Location":
    st.sidebar.subheader("🌐 Auto-Detect Location")
    
    if st.sidebar.button("🌍 Detect My Current Location", type="primary", help="Uses IP geolocation to find your location"):
        with st.spinner("🔍 Detecting your current location..."):
            try:
                import requests
                response = requests.get("https://ipapi.co/json/", timeout=10)
                if response.status_code == 200:
                    location_data = response.json()
                    detected_lat = float(location_data.get('latitude', 0))
                    detected_lon = float(location_data.get('longitude', 0))
                    detected_city = location_data.get('city', '')
                    detected_region = location_data.get('region', '')
                    detected_country = location_data.get('country_name', '')
                    
                    if detected_city and detected_region:
                        detected_name = f"{detected_city}, {detected_region}, {detected_country}"
                    elif detected_city:
                        detected_name = f"{detected_city}, {detected_country}"
                    else:
                        detected_name = f"{detected_country}" if detected_country else "Your Location"
                    
                    st.session_state.selected_latitude = detected_lat
                    st.session_state.selected_longitude = detected_lon
                    st.session_state.selected_location_name = detected_name
                    
                    st.sidebar.success(f"✅ Location detected successfully!")
                    st.sidebar.info(f"📍 **{detected_name}**\n🗺️ {detected_lat:.4f}°, {detected_lon:.4f}°")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Could not detect location automatically.")
            except Exception as e:
                st.sidebar.error(f"❌ Location detection failed: {str(e)}")

# Method 3: Enter coordinates manually
elif location_method == "📍 Enter Coordinates Manually":
    st.sidebar.subheader("📍 Manual Coordinates")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        manual_lat = st.number_input("Latitude", value=st.session_state.selected_latitude, format="%.4f", help="Enter latitude (-90 to 90)")
    with col2:
        manual_lon = st.number_input("Longitude", value=st.session_state.selected_longitude, format="%.4f", help="Enter longitude (-180 to 180)")
    
    if st.sidebar.button("🔍 Get Location Name", help="Find the place name for these coordinates"):
        with st.spinner("🔍 Finding location name..."):
            detected_name = weather_service.get_location_name(manual_lat, manual_lon)
            if detected_name:
                st.session_state.selected_latitude = manual_lat
                st.session_state.selected_longitude = manual_lon
                st.session_state.selected_location_name = detected_name
                st.sidebar.success(f"✅ Location identified: **{detected_name}**")
                st.rerun()

# Display current selected location
st.sidebar.markdown("---")
st.sidebar.subheader("📍 Current Location")
st.sidebar.success(f"**{st.session_state.selected_location_name}**")
st.sidebar.info(f"🗺️ **Coordinates:** {st.session_state.selected_latitude:.4f}°, {st.session_state.selected_longitude:.4f}°")

latitude = st.session_state.selected_latitude
longitude = st.session_state.selected_longitude
location_name = st.session_state.selected_location_name

# Crop selection with full categories
st.sidebar.header("🌱 Crop Information")

crop_categories = {
    "🌾 Grains & Cereals": [
        "Wheat", "Corn", "Rice", "Soybeans", "Barley", "Oats", "Millet", "Sorghum", 
        "Quinoa", "Rye", "Buckwheat", "Amaranth", "Pearl Millet", "Finger Millet", 
        "Foxtail Millet", "Proso Millet", "Triticale", "Teff"
    ],
    "🍎 Fruits": [
        "Apple", "Mango", "Orange", "Grapes", "Banana", "Coconut", "Pineapple", 
        "Papaya", "Guava", "Pomegranate", "Watermelon", "Muskmelon", "Lemon", 
        "Lime", "Grapefruit", "Avocado", "Kiwi", "Dragon Fruit", "Passion Fruit", 
        "Fig", "Date Palm", "Jackfruit", "Litchi", "Rambutan", "Custard Apple", 
        "Strawberry", "Blueberry", "Blackberry", "Raspberry", "Gooseberry", 
        "Cherry", "Plum", "Peach", "Apricot", "Pear"
    ],
    "🥕 Vegetables": [
        "Tomatoes", "Potatoes", "Lettuce", "Carrots", "Onions", "Cucumbers", "Peppers", 
        "Spinach", "Broccoli", "Cabbage", "Beans", "Peas", "Squash", "Eggplant", 
        "Radishes", "Cauliflower", "Okra", "Beetroot", "Turnip", "Sweet Potato", 
        "Pumpkin", "Zucchini", "Bell Pepper", "Hot Pepper", "Kale", "Brussels Sprouts", 
        "Asparagus", "Artichoke", "Celery", "Leek", "Fennel", "Chard", "Arugula", 
        "Bok Choy", "Watercress", "Collard Greens", "Mustard Greens", "Bitter Gourd", 
        "Bottle Gourd", "Ridge Gourd", "Snake Gourd", "Ash Gourd", "Ivy Gourd", 
        "Pointed Gourd", "Drumstick", "Cluster Beans", "French Beans", "Broad Beans"
    ],
    "🌸 Flowers": [
        "Sunflower", "Marigold", "Rose", "Jasmine", "Chrysanthemum", "Dahlia", 
        "Carnation", "Gladiolus", "Tuberose", "Lily", "Lotus", "Hibiscus", 
        "Ixora", "Bougainvillea", "Petunia", "Zinnia", "Cosmos", "Salvia", 
        "Celosia", "Anthurium", "Orchid", "Bird of Paradise", "Heliconia", 
        "Gerbera", "Lavender", "Calendula", "Nasturtium", "Pansy", "Viola"
    ],
    "🌿 Herbs & Spices": [
        "Ginger", "Garlic", "Coriander", "Mint", "Fenugreek", "Mustard", 
        "Green Chili", "Turmeric", "Cumin", "Cardamom", "Cinnamon", "Clove", 
        "Black Pepper", "Nutmeg", "Mace", "Star Anise", "Bay Leaf", "Curry Leaf", 
        "Holy Basil", "Sweet Basil", "Oregano", "Thyme", "Rosemary", "Sage", 
        "Parsley", "Cilantro", "Dill", "Chives", "Tarragon", "Marjoram", 
        "Fennel Seeds", "Carom Seeds", "Nigella Seeds", "Poppy Seeds", "Sesame Seeds",
        "Vanilla", "Saffron", "Asafoetida", "Dried Red Chili"
    ],
    "🏭 Cash Crops": [
        "Cotton", "Sugarcane", "Groundnut", "Sesame", "Safflower", "Castor", 
        "Cashew", "Tobacco", "Coffee", "Tea", "Rubber", "Coconut Palm", "Oil Palm", 
        "Jute", "Hemp", "Flax", "Ramie", "Sisal", "Cocoa", "Black Pepper Vine", 
        "Betel Nut", "Cardamom", "Cinnamon Tree", "Clove Tree", "Nutmeg Tree",
        "Indigo", "Henna", "Aloe Vera", "Stevia", "Moringa"
    ]
}

selected_category = st.sidebar.selectbox(
    "Select crop category",
    list(crop_categories.keys())
)

crop_type = st.sidebar.selectbox(
    "Select your crop",
    crop_categories[selected_category]
)

area_acres = st.sidebar.number_input("Farm Area (acres)", value=10.0, min_value=0.1, step=0.5)

# Main tabs with all features
tabs = st.tabs([
    "🌤️ Weather", 
    "💰 Prices", 
    "💵 Finance", 
    "💧 Irrigation",
    "📅 Calendar",
    "🔄 Rotation",
    "🧪 Fertilizer",
    "📊 Compare",
    "🔧 Tools"
])

# Tab 1: Weather Monitor
with tabs[0]:
    st.header("🌤️ Weather Monitor")
    
    current_weather = weather_service.get_current_weather(latitude, longitude)
    
    if current_weather:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🌡️ Temperature", f"{current_weather['temperature']}°C")
        with col2:
            st.metric("💧 Humidity", f"{current_weather['humidity']}%")
        with col3:
            st.metric("🌧️ Precipitation", f"{current_weather['precipitation']} mm")
        with col4:
            st.metric("💨 Wind Speed", f"{current_weather['wind_speed']} km/h")
        
        # Export weather data
        if st.button("📥 Export Weather Data"):
            forecast = weather_service.get_daily_forecast(latitude, longitude, 7)
            if forecast:
                df = pd.DataFrame(forecast)
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "weather_data.csv",
                    "text/csv",
                    key='download-weather-csv'
                )

# Tab 2: Price Predictions (keep existing)
with tabs[1]:
    st.header("💰 Price Predictions")
    price_data = price_service.get_current_price(crop_type)
    if price_data and 'current' in price_data:
        st.metric(
            f"{crop_type} Price",
            f"₹{price_data['current']:.2f}/kg",
            f"{price_data['change']:+.1f}%"
        )

# Tab 3: Financial Calculator
with tabs[2]:
    st.header("💵 Profit & Financial Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cost Estimation")
        cost_data = financial_calc.calculate_total_cost(crop_type, area_acres)
        
        st.metric("Total Cost", f"₹{cost_data['total_cost']:,.0f}")
        st.metric("Cost per Acre", f"₹{cost_data['total_per_acre']:,.0f}")
        
        # Cost breakdown
        st.write("**Cost Breakdown:**")
        breakdown_df = pd.DataFrame([
            {"Category": k.title(), "Amount (₹)": v, "Percentage": f"{cost_data['breakdown_percent'][k]:.1f}%"}
            for k, v in cost_data['costs_per_acre'].items()
        ])
        st.dataframe(breakdown_df, use_container_width=True)
    
    with col2:
        st.subheader("Profit Analysis")
        yield_qty = st.number_input("Expected Yield (quintals)", value=150.0, min_value=0.0)
        selling_price = st.number_input("Selling Price (₹/quintal)", value=2000.0, min_value=0.0)
        
        if st.button("Calculate Profit"):
            profit_data = financial_calc.calculate_profit(
                cost_data['total_cost'],
                yield_qty,
                selling_price
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Revenue", f"₹{profit_data['revenue']:,.0f}")
                st.metric("Profit/Loss", f"₹{profit_data['profit']:,.0f}")
            with col_b:
                st.metric("ROI", f"{profit_data['roi']:.1f}%")
                if profit_data['status'] == 'profit':
                    st.success("✅ Profitable")
                else:
                    st.error("⚠️ Loss")
    
    # Break-even analysis
    st.subheader("📊 Break-even Analysis")
    if yield_qty > 0:
        breakeven = financial_calc.calculate_breakeven(cost_data['total_cost'], yield_qty)
        st.metric("Break-even Price", f"₹{breakeven['breakeven_price']:.2f}/quintal")
        
        st.write("**Target Prices for Different Profit Margins:**")
        target_df = pd.DataFrame([
            {"Profit Margin": k, "Target Price (₹/quintal)": f"{v:.2f}"}
            for k, v in breakeven['target_prices'].items()
        ])
        st.dataframe(target_df, use_container_width=True)

# Tab 4: Irrigation Calculator
with tabs[3]:
    st.header("💧 Irrigation Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Water Requirement")
        temperature = st.slider("Temperature (°C)", 15, 45, 30)
        humidity = st.slider("Humidity (%)", 20, 100, 60)
        rainfall = st.number_input("Recent Rainfall (mm)", 0.0, 200.0, 0.0)
        growth_stage_irr = st.selectbox("Growth Stage", 
            ["initial", "development", "mid_season", "late_season"])
        
        water_req = irrigation_calc.calculate_water_requirement(
            crop_type, area_acres, growth_stage_irr, temperature, humidity, rainfall
        )
        
        st.metric("Daily Water Need", f"{water_req['daily_volume_liters']:,.0f} L")
        st.metric("Weekly Requirement", f"{water_req['weekly_volume_cubic_meters']:.1f} m³")
        
    with col2:
        st.subheader("Irrigation Schedule")
        irrigation_method = st.selectbox("Irrigation Method", 
            ["drip", "sprinkler", "flood", "furrow", "micro_sprinkler"])
        
        schedule = irrigation_calc.irrigation_schedule(crop_type, irrigation_method)
        
        st.info(f"**Recommended:** {schedule['best_method'].title()}")
        st.write(f"**Frequency:** Every {schedule['recommended_frequency_days']} days")
        st.write(f"**Duration:** {schedule['recommended_duration_hours']} hours")
        st.write(f"**Efficiency:** {schedule['efficiency']*100:.0f}%")
        st.success(f"💧 Water saved vs flood: {schedule['water_saved_vs_flood']}")
        
    # Water cost
    st.subheader("💰 Irrigation Cost")
    water_source = st.selectbox("Water Source", ["borewell", "canal", "river", "well", "tank"])
    cost_calc = irrigation_calc.calculate_irrigation_cost(
        water_req['weekly_volume_liters'], water_source
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pumping Hours", f"{cost_calc['pumping_hours']:.1f} hrs")
    with col2:
        st.metric("Electricity Cost", f"₹{cost_calc['electricity_cost']:.2f}")
    with col3:
        st.metric("Total Weekly Cost", f"₹{cost_calc['total_cost']:.2f}")

# Tab 5: Farm Calendar
with tabs[4]:
    st.header("📅 Farm Calendar & Scheduling")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        planting_date = st.date_input("Planting Date", datetime.now())
        schedule = farm_calendar.create_schedule(crop_type, datetime.combine(planting_date, datetime.min.time()))
        
        if 'error' not in schedule:
            st.success(f"**Harvest Date:** {schedule['harvest_date']}")
            st.info(f"**Total Duration:** {schedule['total_duration_days']} days")
            
            # Timeline visualization
            timeline_df = pd.DataFrame(schedule['timeline'])
            st.subheader("📊 Growth Stages Timeline")
            
            for idx, stage in enumerate(schedule['timeline']):
                with st.expander(f"{stage['stage']} ({stage['duration_days']} days)", expanded=idx==0):
                    st.write(f"**Period:** {stage['start_date']} to {stage['end_date']}")
                    st.write("**Activities:**")
                    for activity in stage['activities']:
                        st.write(f"- {activity}")
    
    with col2:
        st.subheader("🗓️ Best Planting Time")
        recommendation = farm_calendar.recommend_planting_date(crop_type, datetime.now().month)
        
        if 'error' not in recommendation:
            st.write(f"**Current Month:** {recommendation['current_month']}")
            st.write(f"**Best Months:** {', '.join(recommendation['best_planting_months'])}")
            st.info(recommendation['recommendation'])

# Tab 6: Crop Rotation
with tabs[5]:
    st.header("🔄 Crop Rotation Planner")
    
    rotation_years = st.slider("Plan for how many years?", 2, 5, 3)
    rotation = rotation_planner.suggest_rotation(crop_type, rotation_years)
    
    st.subheader("📋 Recommended Rotation Sequence")
    for i, year_plan in enumerate(rotation['rotation_plan']):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(f"Year {year_plan['year']}", year_plan['crop'])
        with col2:
            st.write(f"**Family:** {year_plan['family'].title()}")
            st.write(f"**Nitrogen Need:** {year_plan['nitrogen_need'].title()}")
            for benefit in year_plan['benefits']:
                st.write(f"✅ {benefit}")
        st.divider()
    
    st.subheader("🌟 Overall Benefits")
    for benefit in rotation['overall_benefits']:
        st.write(benefit)
    
    # Crop compatibility checker
    st.subheader("🔍 Check Crop Compatibility")
    col1, col2, col3 = st.columns(3)
    with col1:
        crop1 = st.selectbox("Current Crop", ["Wheat", "Rice", "Corn", "Cotton", "Soybeans"])
    with col2:
        crop2 = st.selectbox("Next Crop", ["Wheat", "Rice", "Corn", "Cotton", "Soybeans"], index=1)
    with col3:
        if st.button("Check"):
            compat = rotation_planner.check_compatibility(crop1, crop2)
            st.metric("Compatibility", f"{compat['compatibility_score']:.0f}%")
            st.write(f"**{compat['recommendation']}**")
            for reason in compat['reasons']:
                st.write(reason)

# Tab 7: Fertilizer Calculator
with tabs[6]:
    st.header("🧪 Fertilizer Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("NPK Requirements")
        
        # Soil test option
        has_soil_test = st.checkbox("I have soil test results")
        soil_test = None
        if has_soil_test:
            st.write("Enter available nutrients (kg/acre):")
            col_n, col_p, col_k = st.columns(3)
            with col_n:
                soil_n = st.number_input("Nitrogen", 0.0, 100.0, 20.0)
            with col_p:
                soil_p = st.number_input("Phosphorus", 0.0, 100.0, 15.0)
            with col_k:
                soil_k = st.number_input("Potassium", 0.0, 100.0, 15.0)
            soil_test = {"N": soil_n, "P": soil_p, "K": soil_k}
        
        fert_req = fertilizer_calc.calculate_fertilizer_requirement(
            crop_type, area_acres, soil_test
        )
        
        st.write("**Required NPK (per acre):**")
        npk_df = pd.DataFrame([fert_req['npk_per_acre']])
        st.dataframe(npk_df, use_container_width=True)
        
        st.write("**Total NPK Required:**")
        total_npk_df = pd.DataFrame([fert_req['total_npk_required']])
        st.dataframe(total_npk_df, use_container_width=True)
    
    with col2:
        st.subheader("Fertilizer Recommendation")
        
        prefer_organic = st.checkbox("Prefer Organic Fertilizers")
        
        fert_plan = fertilizer_calc.recommend_fertilizers(
            fert_req['total_npk_required'], 
            area_acres, 
            prefer_organic
        )
        
        st.metric("Total Cost", f"₹{fert_plan['total_cost']:,.2f}")
        st.metric("Cost per Acre", f"₹{fert_plan['cost_per_acre']:,.2f}/acre")
        
        st.write("**Fertilizer Application Plan:**")
        for item in fert_plan['fertilizer_plan']:
            with st.expander(f"{item['fertilizer']}", expanded=True):
                if 'quantity_kg' in item:
                    st.write(f"**Quantity:** {item['quantity_kg']:.2f} kg")
                elif 'quantity_tons' in item:
                    st.write(f"**Quantity:** {item['quantity_tons']:.2f} tons")
                st.write(f"**Cost:** ₹{item['cost']:.2f}")
                st.write(f"**Application:** {item['application']}")
        
        if prefer_organic and 'benefits' in fert_plan:
            st.success("**Organic Benefits:**")
            for benefit in fert_plan['benefits']:
                st.write(f"✅ {benefit}")

# Tab 8: Multi-Crop Comparison
with tabs[7]:
    st.header("📊 Multi-Crop Comparison")
    
    st.write("Compare requirements for different crops:")
    compare_crops = st.multiselect(
        "Select crops to compare",
        ["Wheat", "Rice", "Corn", "Cotton", "Soybeans", "Tomatoes", "Potatoes", "Onions"],
        default=["Wheat", "Rice", "Corn"]
    )
    
    if len(compare_crops) >= 2:
        comparison_data = []
        
        for crop in compare_crops:
            # Get crop requirements
            if hasattr(crop_recommendations, 'crop_requirements') and crop in crop_recommendations.crop_requirements:
                req = crop_recommendations.crop_requirements[crop]
                comparison_data.append({
                    "Crop": crop,
                    "Temp Range": f"{req['temp_range'][0]}-{req['temp_range'][1]}°C",
                    "Optimal Temp": f"{req['optimal_temp'][0]}-{req['optimal_temp'][1]}°C",
                    "Humidity": f"{req['humidity_range'][0]}-{req['humidity_range'][1]}%",
                    "Water Need": req['water_needs']
                })
        
        if comparison_data:
            comp_df = pd.DataFrame(comparison_data)
            st.dataframe(comp_df, use_container_width=True)
            
            # Financial comparison
            st.subheader("💰 Financial Comparison")
            fin_comparison = []
            for crop in compare_crops:
                cost_data = financial_calc.calculate_total_cost(crop, 1)  # Per acre
                fin_comparison.append({
                    "Crop": crop,
                    "Cost/Acre": f"₹{cost_data['total_per_acre']:,.0f}",
                    "Seed": f"₹{cost_data['costs_per_acre'].get('seed', 0):,.0f}",
                    "Fertilizer": f"₹{cost_data['costs_per_acre'].get('fertilizer', 0):,.0f}",
                    "Labor": f"₹{cost_data['costs_per_acre'].get('labor', 0):,.0f}",
                })
            
            fin_df = pd.DataFrame(fin_comparison)
            st.dataframe(fin_df, use_container_width=True)

# Tab 9: Unit Converter & Tools
with tabs[8]:
    st.header("🔧 Unit Converter & Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📏 Area Converter")
        area_value = st.number_input("Value", value=1.0, min_value=0.0, key="area_val")
        col_a, col_b = st.columns(2)
        with col_a:
            from_unit_area = st.selectbox("From", ["acres", "hectares", "sqm", "bigha"], key="from_area")
        with col_b:
            to_unit_area = st.selectbox("To", ["acres", "hectares", "sqm", "bigha"], key="to_area")
        
        converted_area = unit_converter.area_conversion(area_value, from_unit_area, to_unit_area)
        st.success(f"{area_value} {from_unit_area} = **{converted_area:.4f} {to_unit_area}**")
    
    with col2:
        st.subheader("⚖️ Weight Converter")
        weight_value = st.number_input("Value", value=1.0, min_value=0.0, key="weight_val")
        col_a, col_b = st.columns(2)
        with col_a:
            from_unit_weight = st.selectbox("From", ["kg", "quintal", "ton", "pounds"], key="from_weight")
        with col_b:
            to_unit_weight = st.selectbox("To", ["kg", "quintal", "ton", "pounds"], key="to_weight")
        
        converted_weight = unit_converter.weight_conversion(weight_value, from_unit_weight, to_unit_weight)
        st.success(f"{weight_value} {from_unit_weight} = **{converted_weight:.4f} {to_unit_weight}**")
    
    st.subheader("🌡️ Temperature Converter")
    temp_value = st.number_input("Temperature", value=25.0, key="temp_val")
    col_a, col_b = st.columns(2)
    with col_a:
        from_unit_temp = st.selectbox("From", ["celsius", "fahrenheit", "kelvin"], key="from_temp")
    with col_b:
        to_unit_temp = st.selectbox("To", ["celsius", "fahrenheit", "kelvin"], key="to_temp")
    
    converted_temp = unit_converter.temperature_conversion(temp_value, from_unit_temp, to_unit_temp)
    st.success(f"{temp_value}° {from_unit_temp.title()} = **{converted_temp:.2f}° {to_unit_temp.title()}**")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🌾 Agricultural Assistant Pro")
with col2:
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
with col3:
    if st.button("🔄 Refresh All"):
        st.cache_data.clear()
        st.rerun()
