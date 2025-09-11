import streamlit as st

st.title("🌾 Agricultural Assistant - Test")
st.write("If you can see this, the Streamlit setup is working correctly!")

try:
    from weather_service import WeatherService
    from crop_recommendations import CropRecommendations
    from price_service import PriceService
    from utils import format_temperature
    
    st.success("✅ All modules imported successfully!")
    
    # Test basic functionality
    weather_service = WeatherService()
    crop_recommendations = CropRecommendations()
    price_service = PriceService()
    
    st.write("📍 Testing with New York coordinates:")
    lat, lon = 40.7128, -74.0060
    
    # Test weather service
    with st.spinner("Testing weather service..."):
        current_weather = weather_service.get_current_weather(lat, lon)
        if current_weather:
            st.success(f"🌡️ Weather service working! Temperature: {current_weather['temperature']:.1f}°C")
        else:
            st.error("❌ Weather service failed")
    
    # Test price service  
    price = price_service.get_current_price("Wheat")
    if price:
        st.success(f"💰 Price service working! Wheat: ${price['current']:.2f}")
    else:
        st.error("❌ Price service failed")
        
except Exception as e:
    st.error(f"❌ Error: {e}")