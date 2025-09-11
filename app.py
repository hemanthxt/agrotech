import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import requests
import numpy as np

from weather_service import WeatherService
from crop_recommendations import CropRecommendations
from price_service import PriceService
from utils import format_temperature, format_precipitation, get_weather_icon

# Page configuration
st.set_page_config(
    page_title="Agricultural Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def init_services():
    weather_service = WeatherService()
    crop_recommendations = CropRecommendations()
    price_service = PriceService()
    return weather_service, crop_recommendations, price_service

weather_service, crop_recommendations, price_service = init_services()

# Main navigation
st.title("🌾 Agricultural Assistant")
st.markdown("Complete farming solution with weather monitoring and price predictions")

# Sidebar for location input (shared across all tabs)
st.sidebar.header("🌍 Farm Location")

# Location input methods
location_method = st.sidebar.radio(
    "How would you like to set your location?",
    ["🔍 Search by Place Name", "🌐 Auto-Detect Current Location", "📍 Enter Coordinates Manually"],
    index=0
)

# Initialize session state variables
if 'selected_latitude' not in st.session_state:
    st.session_state.selected_latitude = 28.6139  # Default to New Delhi
if 'selected_longitude' not in st.session_state:
    st.session_state.selected_longitude = 77.2090
if 'selected_location_name' not in st.session_state:
    st.session_state.selected_location_name = "New Delhi, Delhi, India"

# Method 1: Search by Place Name
if location_method == "🔍 Search by Place Name":
    st.sidebar.subheader("🔍 Search for Your Location")
    
    # Location search input
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
                
                # Display search results as selectbox
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
                response = requests.get("https://ipapi.co/json/", timeout=10)
                if response.status_code == 200:
                    location_data = response.json()
                    detected_lat = float(location_data.get('latitude', 0))
                    detected_lon = float(location_data.get('longitude', 0))
                    detected_city = location_data.get('city', '')
                    detected_region = location_data.get('region', '')
                    detected_country = location_data.get('country_name', '')
                    
                    # Build location name
                    if detected_city and detected_region:
                        detected_name = f"{detected_city}, {detected_region}, {detected_country}"
                    elif detected_city:
                        detected_name = f"{detected_city}, {detected_country}"
                    else:
                        detected_name = f"{detected_country}" if detected_country else "Your Location"
                    
                    # Update session state
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
        manual_lat = st.number_input(
            "Latitude", 
            value=st.session_state.selected_latitude, 
            format="%.4f", 
            help="Enter latitude (-90 to 90)"
        )
    with col2:
        manual_lon = st.number_input(
            "Longitude", 
            value=st.session_state.selected_longitude, 
            format="%.4f", 
            help="Enter longitude (-180 to 180)"
        )
    
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

# Set final coordinates for use in the app
latitude = st.session_state.selected_latitude
longitude = st.session_state.selected_longitude
location_name = st.session_state.selected_location_name

# Crop selection with categories
st.sidebar.header("Crop Information")

# Define crop categories with expanded selections
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

# Create category selection
selected_category = st.sidebar.selectbox(
    "Select crop category",
    list(crop_categories.keys())
)

# Create crop selection based on category
crop_type = st.sidebar.selectbox(
    "Select your crop",
    crop_categories[selected_category]
)

# Growth stage
growth_stage = st.sidebar.selectbox(
    "Growth Stage",
    ["Planting", "Germination", "Vegetative", "Flowering", "Fruiting", "Maturation", "Harvest"]
)

# Refresh button
if st.sidebar.button("🔄 Refresh Weather Data"):
    st.cache_data.clear()
    st.rerun()

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh (5 minutes)", value=False)

# Create tabs for navigation
tab1, tab2 = st.tabs(["🌤️ Weather Monitor", "💰 Price Predictor"])

# Tab 1: Weather Monitor
with tab1:
    st.header("🌤️ Weather Monitoring & Crop Recommendations")
    
    # Main content
    try:
        # Fetch weather data
        with st.spinner("Fetching weather data..."):
            current_weather = weather_service.get_current_weather(latitude, longitude)
            daily_forecast = weather_service.get_daily_forecast(latitude, longitude, days=7)
            hourly_forecast = weather_service.get_hourly_forecast(latitude, longitude, hours=24)
    
        if current_weather and daily_forecast and hourly_forecast:
            # Current conditions section with enhanced location info
            st.header(f"🏠 Current Conditions - {location_name}")
            st.caption(f"📍 Coordinates: {latitude:.4f}°, {longitude:.4f}°")
        
            col1, col2, col3, col4 = st.columns(4)
        
            with col1:
                st.metric(
                    label="🌡️ Temperature",
                    value=f"{current_weather['temperature']:.1f}°C",
                    delta=f"{current_weather['temperature'] - daily_forecast[0]['temp_min']:.1f}°C from min"
                )
        
            with col2:
                st.metric(
                    label="💧 Humidity",
                    value=f"{current_weather['humidity']:.0f}%",
                    delta=None
                )
        
            with col3:
                st.metric(
                    label="🌧️ Precipitation",
                    value=f"{current_weather['precipitation']:.1f} mm",
                    delta=None
                )
        
            with col4:
                st.metric(
                    label="💨 Wind Speed",
                    value=f"{current_weather['wind_speed']:.1f} km/h",
                    delta=None
                )
        
            # Weather alerts
            alerts = weather_service.check_weather_alerts(current_weather, daily_forecast[0])
            if alerts:
                st.header("⚠️ Weather Alerts")
                for alert in alerts:
                    if alert['severity'] == 'warning':
                        st.warning(f"**{alert['type']}**: {alert['message']}")
                    elif alert['severity'] == 'error':
                        st.error(f"**{alert['type']}**: {alert['message']}")
                    else:
                        st.info(f"**{alert['type']}**: {alert['message']}")
            
            # Crop recommendations
            st.header(f"🌱 Recommendations for {crop_type} ({growth_stage})")
            recommendations = crop_recommendations.get_recommendations(
                crop_type, growth_stage, current_weather, daily_forecast[0]
            )
            
            rec_col1, rec_col2 = st.columns(2)
            
            with rec_col1:
                st.subheader("🚿 Irrigation")
                if recommendations['irrigation']['needed']:
                    st.success(f"✅ {recommendations['irrigation']['message']}")
                else:
                    st.info(f"ℹ️ {recommendations['irrigation']['message']}")
                
                st.subheader("🌾 Field Activities")
                for activity in recommendations['activities']:
                    if activity['recommended']:
                        st.success(f"✅ {activity['activity']}: {activity['reason']}")
                    else:
                        st.warning(f"⚠️ Avoid {activity['activity']}: {activity['reason']}")
            
            with rec_col2:
                st.subheader("🛡️ Disease Risk")
                risk_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                st.markdown(f"{risk_color[recommendations['disease_risk']['level']]} **{recommendations['disease_risk']['level']} Risk**")
                st.write(recommendations['disease_risk']['message'])
                
                st.subheader("📝 General Advice")
                for advice in recommendations['general_advice']:
                    st.info(advice)
            
            # Charts section
            col1, col2 = st.columns(2)
            
            with col1:
                # Temperature trend
                st.subheader("📈 24-Hour Temperature Trend")
                temp_df = pd.DataFrame({
                    'Time': [datetime.fromisoformat(h['time'].replace('Z', '+00:00')) for h in hourly_forecast],
                    'Temperature': [h['temperature'] for h in hourly_forecast]
                })
                
                fig_temp = px.line(temp_df, x='Time', y='Temperature', 
                                  title='Temperature (°C)',
                                  line_shape='spline')
                fig_temp.update_layout(height=300)
                st.plotly_chart(fig_temp, width="stretch")
            
            with col2:
                # Precipitation forecast
                st.subheader("🌧️ 24-Hour Precipitation Forecast")
                precip_df = pd.DataFrame({
                    'Time': [datetime.fromisoformat(h['time'].replace('Z', '+00:00')) for h in hourly_forecast],
                    'Precipitation': [h['precipitation'] for h in hourly_forecast]
                })
                
                fig_precip = px.bar(precip_df, x='Time', y='Precipitation',
                                   title='Precipitation (mm)',
                                   color='Precipitation',
                                   color_continuous_scale='Blues')
                fig_precip.update_layout(height=300)
                st.plotly_chart(fig_precip, width="stretch")
            
            # 7-day forecast
            st.header("📅 7-Day Forecast")
            forecast_data = []
            for day in daily_forecast:
                date = datetime.fromisoformat(day['date'])
                forecast_data.append({
                    'Date': date.strftime('%m/%d'),
                    'Day': date.strftime('%A'),
                    'High': f"{day['temp_max']:.0f}°C",
                    'Low': f"{day['temp_min']:.0f}°C",
                    'Precipitation': f"{day['precipitation']:.1f}mm",
                    'Humidity': f"{day['humidity']:.0f}%",
                    'Wind': f"{day['wind_speed']:.0f} km/h"
                })
            
            forecast_df = pd.DataFrame(forecast_data)
            st.dataframe(forecast_df, width="stretch", hide_index=True)
            
            # Growing conditions summary
            st.header("🌱 Growing Conditions Summary")
            conditions = crop_recommendations.analyze_growing_conditions(crop_type, current_weather, daily_forecast)
            
            condition_col1, condition_col2, condition_col3 = st.columns(3)
            
            with condition_col1:
                st.metric("Overall Conditions", conditions['overall'], conditions['overall_trend'])
            
            with condition_col2:
                st.metric("Temperature Suitability", conditions['temperature'])
            
            with condition_col3:
                st.metric("Moisture Levels", conditions['moisture'])
        
        else:
            st.error("Failed to fetch weather data. Please check your internet connection and try again.")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your location coordinates and try again.")

# Tab 2: Price Predictor
with tab2:
    st.header("💰 Crop Price Prediction")
    st.markdown("Get real-time prices and predictions for your crops")
    
    # Price analysis for selected crop
    with st.spinner("Loading price data..."):
        current_price = price_service.get_current_price(crop_type)
        market_analysis = price_service.get_market_analysis(crop_type)
        selling_advice = price_service.get_best_selling_time(crop_type)
    
    if current_price:
        # Current price display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                f"💰 Current {crop_type} Price",
                f"₹{current_price['current']:.2f}/kg",
                f"{current_price['change']:+.1f}%",
                delta_color="normal"
            )
        
        with col2:
            if market_analysis['status'] == 'success':
                st.metric(
                    "📊 vs 30-Day Avg",
                    f"{market_analysis['vs_30day_avg']:+.1f}%",
                    None
                )
        
        with col3:
            if market_analysis['status'] == 'success':
                trend_emoji = "📈" if market_analysis['trend'] == 'upward' else "📉" if market_analysis['trend'] == 'downward' else "➡️"
                st.metric(
                    "📈 Market Trend",
                    f"{trend_emoji} {market_analysis['trend'].title()}",
                    None
                )
    
    # Enhanced Price Analysis Dashboard
    st.markdown("---")
    st.subheader("📊 Price Analysis Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Historical Price Trend (30 Days)")
        historical_data = price_service.generate_historical_data(crop_type, 30)
        if historical_data is not None:
            # Create enhanced historical price chart
            fig_history = go.Figure()
            
            # Add main price line
            fig_history.add_trace(go.Scatter(
                x=historical_data['Date'],
                y=historical_data['Price'],
                mode='lines+markers',
                name=f'{crop_type} Price',
                line=dict(color='#2E86AB', width=3),
                marker=dict(size=4, color='#2E86AB'),
                hovertemplate='<b>%{x|%d %b %Y}</b><br>Price: ₹<b>%{y:.2f}</b>/kg<extra></extra>'
            ))
            
            # Add trend line
            if len(historical_data) > 1:
                z = np.polyfit(range(len(historical_data)), historical_data['Price'], 1)
                p = np.poly1d(z)
                trend_line = p(range(len(historical_data)))
                
                fig_history.add_trace(go.Scatter(
                    x=historical_data['Date'],
                    y=trend_line,
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='#E74C3C', width=2, dash='dash'),
                    hovertemplate='Trend: ₹<b>%{y:.2f}</b>/kg<extra></extra>'
                ))
            
            # Enhanced layout
            fig_history.update_layout(
                title=dict(
                    text=f'<b>{crop_type} - 30 Day Price History</b>',
                    font=dict(size=16, color='#2C3E50'),
                    x=0.5
                ),
                xaxis=dict(
                    title='<b>Date</b>',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.2)',
                    tickformat='%d %b',
                    tickfont=dict(size=11)
                ),
                yaxis=dict(
                    title='<b>Price (₹/kg)</b>',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.2)',
                    tickformat='.2f',
                    tickfont=dict(size=11)
                ),
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    bgcolor="rgba(255,255,255,0.8)"
                ),
                plot_bgcolor='rgba(248,249,250,0.8)',
                paper_bgcolor='white',
                margin=dict(t=80, l=60, r=40, b=60),
                font=dict(family="Arial, sans-serif")
            )
            
            st.plotly_chart(fig_history, use_container_width=True)
            
            # Price statistics in a nice format
            avg_price = historical_data['Price'].mean()
            max_price = historical_data['Price'].max()
            min_price = historical_data['Price'].min()
            volatility = historical_data['Price'].std()
            
            st.markdown("**📊 Price Statistics:**")
            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
            with col_stats1:
                st.metric("📊 Average", f"₹{avg_price:.2f}", help="30-day average price")
            with col_stats2:
                st.metric("📈 Peak", f"₹{max_price:.2f}", help="Highest price in 30 days")
            with col_stats3:
                st.metric("📉 Low", f"₹{min_price:.2f}", help="Lowest price in 30 days")
            with col_stats4:
                st.metric("🌊 Volatility", f"₹{volatility:.2f}", help="Price standard deviation")
        else:
            st.info("📊 Historical price data is not available for this crop")
    
    with col2:
        st.markdown("#### 🔮 Price Forecast (Next 7 Days)")
        predictions = price_service.predict_future_prices(crop_type, 7)
        if predictions is not None:
            # Create enhanced forecast chart
            fig_forecast = go.Figure()
            
            # Add current price marker
            if current_price:
                fig_forecast.add_trace(go.Scatter(
                    x=[datetime.now()],
                    y=[current_price['current']],
                    mode='markers',
                    name='Current Price',
                    marker=dict(size=15, color='#27AE60', symbol='circle', line=dict(width=2, color='white')),
                    hovertemplate='<b>Current Price</b><br>₹<b>%{y:.2f}</b>/kg<extra></extra>'
                ))
            
            # Add forecast line with markers
            fig_forecast.add_trace(go.Scatter(
                x=predictions['Date'],
                y=predictions['Predicted_Price'],
                mode='lines+markers',
                name='Price Forecast',
                line=dict(color='#F39C12', width=3),
                marker=dict(size=6, color='#F39C12'),
                hovertemplate='<b>%{x|%d %b}</b><br>Predicted: ₹<b>%{y:.2f}</b>/kg<extra></extra>'
            ))
            
            # Add confidence interval
            upper_bound = predictions['Predicted_Price'] * 1.08
            lower_bound = predictions['Predicted_Price'] * 0.92
            
            fig_forecast.add_trace(go.Scatter(
                x=predictions['Date'],
                y=upper_bound,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig_forecast.add_trace(go.Scatter(
                x=predictions['Date'],
                y=lower_bound,
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor='rgba(243, 156, 18, 0.2)',
                name='Confidence Range',
                showlegend=True,
                hovertemplate='Range: ₹<b>%{y:.2f}</b>/kg<extra></extra>'
            ))
            
            # Enhanced layout for forecast
            fig_forecast.update_layout(
                title=dict(
                    text=f'<b>{crop_type} - 7 Day Price Forecast</b>',
                    font=dict(size=16, color='#2C3E50'),
                    x=0.5
                ),
                xaxis=dict(
                    title='<b>Date</b>',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.2)',
                    tickformat='%d %b',
                    tickfont=dict(size=11)
                ),
                yaxis=dict(
                    title='<b>Predicted Price (₹/kg)</b>',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.2)',
                    tickformat='.2f',
                    tickfont=dict(size=11)
                ),
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    bgcolor="rgba(255,255,255,0.8)"
                ),
                plot_bgcolor='rgba(248,249,250,0.8)',
                paper_bgcolor='white',
                margin=dict(t=80, l=60, r=40, b=60),
                font=dict(family="Arial, sans-serif")
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Forecast insights
            if len(predictions) > 1:
                forecast_change = ((predictions['Predicted_Price'].iloc[-1] - predictions['Predicted_Price'].iloc[0]) / predictions['Predicted_Price'].iloc[0]) * 100
                best_price_day = predictions.loc[predictions['Predicted_Price'].idxmax()]
                
                st.markdown("**🎯 Forecast Insights:**")
                col_insight1, col_insight2 = st.columns(2)
                with col_insight1:
                    change_color = "normal" if abs(forecast_change) < 5 else "inverse"
                    st.metric("📊 Expected Change", f"{forecast_change:+.1f}%", 
                             delta_color=change_color, help="7-day price change prediction")
                with col_insight2:
                    st.metric("📅 Best Day to Sell", 
                             best_price_day['Date'].strftime("%d %b"), 
                             f"₹{best_price_day['Predicted_Price']:.2f}/kg",
                             help="Day with highest predicted price")
        else:
            st.info("🔮 Price forecast data is not available for this crop")
    
    # Market analysis and recommendations
    if market_analysis['status'] == 'success':
        st.header("📊 Market Analysis")
        
        for recommendation in market_analysis['recommendations']:
            if '🟢' in recommendation:
                st.success(recommendation)
            elif '🔴' in recommendation:
                st.error(recommendation)
            elif '🟡' in recommendation:
                st.warning(recommendation)
            else:
                st.info(recommendation)
    
    # Selling recommendations
    if selling_advice['status'] == 'success':
        st.header("💡 Selling Recommendations")
        
        if selling_advice['action'] == 'sell_now':
            st.success(f"🎯 **{selling_advice['recommendation']}**")
        elif selling_advice['action'] == 'wait':
            st.info(f"⏳ **{selling_advice['recommendation']}**")
        elif selling_advice['action'] == 'hold':
            st.warning(f"📈 **{selling_advice['recommendation']}**")
        else:
            st.info(f"👀 **{selling_advice['recommendation']}**")
        
        # Additional details
        st.markdown("### Selling Strategy Details:")
        st.write(f"🎯 **Optimal selling date:** {selling_advice['optimal_date']}")
        st.write(f"📅 **Days to wait:** {selling_advice['days_to_wait']} days")
        st.write(f"💰 **Expected price:** ₹{selling_advice['expected_price']:.2f}/kg")
        st.write(f"📊 **Potential gain:** {selling_advice['potential_gain_percent']:+.1f}%")

# Auto-refresh functionality
if auto_refresh:
    time.sleep(300)  # 5 minutes
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🌾 Agricultural Assistant | Weather data by Open-Meteo | Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
