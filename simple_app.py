import streamlit as st
import pandas as pd
from datetime import datetime
from price_service import PriceService
from crop_recommendations import CropRecommendations

# Page configuration
st.set_page_config(
    page_title="AgroPrice Pro - Agricultural Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E8B57, #228B22);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .price-card {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        color: white;
    }
    .info-card {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        color: white;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa, #e9ecef);
    }
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .footer {
        background: linear-gradient(90deg, #2E8B57, #228B22);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
@st.cache_resource
def init_services():
    price_service = PriceService()
    crop_recommendations = CropRecommendations()
    return price_service, crop_recommendations

price_service, crop_recommendations = init_services()

# CATEGORIZED CROP SYSTEM WITH COMPREHENSIVE IMAGE MAPPING
crop_categories = {
    "🌾 GRAINS": {
        "Wheat": "attached_assets/generated_images/Wheat_crop_field_photo_a6cc5c03.png",
        "Corn": "attached_assets/generated_images/Fresh_corn_cobs_photo_8ac50baf.png", 
        "Rice": "attached_assets/generated_images/Rice_paddy_field_photo_df0c5e76.png",
        "Soybeans": "attached_assets/generated_images/Soybean_pods_photo_7438b4e9.png",
        "Groundnut": None,
        "Sesame": None,
        "Safflower": None,
        "Castor": None
    },
    "🥬 VEGETABLES": {
        "Tomatoes": "attached_assets/generated_images/Fresh_red_tomatoes_photo_95939cf3.png",
        "Potatoes": "attached_assets/generated_images/Fresh_potatoes_photo_cdc62b3b.png",
        "Carrots": "attached_assets/generated_images/Fresh_orange_carrots_photo_fa400f49.png",
        "Lettuce": "attached_assets/generated_images/Fresh_lettuce_heads_photo_2254c1e5.png",
        "Onions": "attached_assets/generated_images/Fresh_onions_photo_78b91562.png",
        "Cucumbers": "attached_assets/generated_images/Fresh_cucumbers_photo_13050652.png",
        "Peppers": "attached_assets/generated_images/Colorful_bell_peppers_photo_9c597ded.png",
        "Spinach": "attached_assets/generated_images/Fresh_spinach_leaves_photo_08a2f73e.png",
        "Broccoli": "attached_assets/generated_images/Fresh_broccoli_head_photo_d851602b.png",
        "Cabbage": "attached_assets/generated_images/Fresh_cabbage_head_photo_a1ba882b.png",
        "Beans": "attached_assets/generated_images/Fresh_green_beans_photo_04bda086.png",
        "Peas": "attached_assets/generated_images/Fresh_pea_pods_photo_a0e38cd9.png",
        "Eggplant": "attached_assets/generated_images/Fresh_eggplant_photo_f694a57f.png",
        "Garlic": "attached_assets/generated_images/Fresh_garlic_bulbs_photo_1f567066.png",
        "Green Chili": "attached_assets/generated_images/Green_chili_peppers_photo_a4e5c601.png",
        "Ginger": "attached_assets/generated_images/Fresh_ginger_root_photo_db6f1714.png",
        "Cauliflower": None,
        "Okra": None,
        "Beetroot": None,
        "Turnip": None,
        "Radishes": None,
        "Squash": None
    },
    "🍎 FRUITS": {
        "Banana": "attached_assets/generated_images/Yellow_banana_bunch_photo_984676e5.png",
        "Mango": "attached_assets/generated_images/Ripe_mango_fruits_photo_2e4a2544.png",
        "Apple": "attached_assets/generated_images/Fresh_red_apples_photo_54155f10.png",
        "Grapes": "attached_assets/generated_images/Fresh_grape_bunches_photo_f16c080d.png",
        "Orange": "attached_assets/generated_images/Fresh_oranges_photo_3f68a084.png",
        "Coconut": "attached_assets/generated_images/Fresh_coconut_photo_cbdf79c0.png",
        "Cashew": None
    },
    "🌸 FLOWERS": {
        "Roses": "attached_assets/generated_images/Beautiful_red_roses_photo_2ad49868.png",
        "Sunflower": "attached_assets/generated_images/Bright_sunflower_photo_884810e2.png",
        "Marigold": "attached_assets/generated_images/Colorful_marigold_flowers_photo_0a6a0490.png",
        "Jasmine": None,
        "Chrysanthemum": None,
        "Lotus": None
    }
}

# Additional crops for comprehensive coverage
other_crops = {
    "Cotton": "attached_assets/generated_images/Cotton_plant_photo_d589b68e.png",
    "Sugarcane": None,
    "Turmeric": None,
    "Coriander": None,
    "Mint": None,
    "Fenugreek": None,
    "Mustard": None
}

# Main title with custom styling
st.markdown("""
<div class="main-header">
    <h1>🌾 AgroPrice Pro</h1>
    <h3>Your Complete Agricultural Market Assistant</h3>
    <p>Monitor real-time crop prices • Get expert growing recommendations • Maximize your profits</p>
</div>
""", unsafe_allow_html=True)

# CATEGORIZED CROP SELECTION INTERFACE
st.sidebar.markdown("## 🌱 Select Your Crop by Category")
st.sidebar.markdown("Choose from organized categories to get instant market data and growing insights")

# Category selection
selected_category = st.sidebar.selectbox(
    "Choose Category",
    list(crop_categories.keys())
)

# Crop selection within category
crops_in_category = list(crop_categories[selected_category].keys())
crop_type = st.sidebar.selectbox(
    f"Select {selected_category.split(' ')[1]} Crop",
    crops_in_category
)

# Display selected crop image in sidebar with category info
st.sidebar.markdown("### 📸 Selected Crop")
crop_image = crop_categories[selected_category].get(crop_type)

if crop_image:
    st.sidebar.image(crop_image, caption=f"{crop_type}", width=200)
    st.sidebar.success(f"✅ {selected_category}")
else:
    st.sidebar.info("📷 Image coming soon")
    st.sidebar.info(f"📋 Category: {selected_category}")

st.sidebar.markdown(f"**Current Selection:** {crop_type}")
st.sidebar.markdown(f"**Category:** {selected_category}")

# Growth stage
growth_stage = st.sidebar.selectbox(
    "Growth Stage",
    ["Planting", "Germination", "Vegetative", "Flowering", "Fruiting", "Maturation", "Harvest"]
)

# Main content area with tabs for better organization
tab1, tab2, tab3 = st.tabs(["💰 Market Prices", "🌱 Growing Guide", "📊 Analytics"])

with tab1:
    st.markdown(f"""
    <div class="price-card">
        <h2>💰 {crop_type} Market Information</h2>
        <p>Real-time pricing and market trends for your selected crop</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current price
    current_price = price_service.get_current_price(crop_type)
    
    if current_price:
        # Display current price in a styled container
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                f"💵 Current Price",
                f"₹{current_price['current']:.2f}/kg",
                f"{current_price['change']:+.1f}%",
                delta_color="normal"
            )
        with col2:
            market_analysis = price_service.get_market_analysis(crop_type)
            if market_analysis['status'] == 'success':
                st.metric(
                    "📈 30-Day Trend",
                    f"{market_analysis['vs_30day_avg']:+.1f}%",
                    f"{market_analysis['trend'].title()}"
                )
        with col3:
            st.metric(
                "📅 Last Updated",
                datetime.now().strftime('%d %b'),
                datetime.now().strftime('%H:%M')
            )
        
        
        # Market analysis in styled container
        st.markdown("### 📊 Market Analysis & Insights")
        if market_analysis['status'] == 'success':
            for recommendation in market_analysis['recommendations']:
                if '🟢' in recommendation:
                    st.success(recommendation)
                elif '🔴' in recommendation:
                    st.error(recommendation)
                elif '🟡' in recommendation:
                    st.warning(recommendation)
                else:
                    st.info(recommendation)
        
        # Selling advice in an expandable section
        with st.expander("💡 Intelligent Selling Strategy", expanded=True):
            selling_advice = price_service.get_best_selling_time(crop_type)
            if selling_advice['status'] == 'success':
                if selling_advice['action'] == 'sell_now':
                    st.success(f"🎯 **{selling_advice['recommendation']}**")
                elif selling_advice['action'] == 'wait':
                    st.info(f"⏳ **{selling_advice['recommendation']}**")
                elif selling_advice['action'] == 'hold':
                    st.warning(f"📈 **{selling_advice['recommendation']}**")
                else:
                    st.info(f"👀 **{selling_advice['recommendation']}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"🎯 **Optimal Date:** {selling_advice['optimal_date']}")
                    st.write(f"📅 **Days to Wait:** {selling_advice['days_to_wait']} days")
                with col2:
                    st.write(f"💰 **Expected Price:** ₹{selling_advice['expected_price']:.2f}/kg")
                    st.write(f"📊 **Potential Gain:** {selling_advice['potential_gain_percent']:+.1f}%")
    else:
        st.error(f"❌ Price data not available for {crop_type}")

with tab2:
    st.markdown(f"""
    <div class="info-card">
        <h2>🌱 {crop_type} Growing Guide</h2>
        <p>Expert agricultural recommendations and optimal growing conditions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display large crop image and category info
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        crop_image = crop_categories[selected_category].get(crop_type)
        if crop_image:
            st.image(crop_image, caption=f"{crop_type}", width=300)
        else:
            st.info("📷 Image coming soon")
    
    with col_info:
        # Category-based descriptions
        category_descriptions = {
            "🌾 GRAINS": "Staple food crops providing essential carbohydrates, proteins, and nutrition for human consumption",
            "🥬 VEGETABLES": "Fresh produce rich in vitamins, minerals, dietary fiber, and essential nutrients for healthy living",
            "🍎 FRUITS": "Sweet, nutritious fruits packed with vitamins, antioxidants, and natural sugars for energy",
            "🌸 FLOWERS": "Beautiful ornamental crops grown for decoration, ceremonies, and aesthetic purposes"
        }
        
        # Count crops in category
        crops_count = len(crop_categories[selected_category])
        available_images = sum(1 for img in crop_categories[selected_category].values() if img is not None)
        
        st.markdown(f"### {selected_category}")
        st.write(category_descriptions.get(selected_category, "Important agricultural produce with commercial value"))
        st.markdown(f"**Current Growth Stage:** {growth_stage}")
        st.markdown(f"**Category:** {selected_category.split(' ')[1]} Crop")
        st.markdown(f"**Available in Category:** {crops_count} varieties")
        st.markdown(f"**With Photos:** {available_images}/{crops_count} crops")
    
    st.markdown("---")
    
    # Get crop requirements
    crop_reqs = crop_recommendations.crop_requirements.get(crop_type, {})
    
    if crop_reqs:
        # Growing conditions in organized cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌡️ Temperature Requirements")
        
            temp_range = crop_reqs.get('temp_range', (0, 0))
            optimal_temp = crop_reqs.get('optimal_temp', (0, 0))
            st.metric("Temperature Range", f"{temp_range[0]}°C - {temp_range[1]}°C")
            st.metric("Optimal Range", f"{optimal_temp[0]}°C - {optimal_temp[1]}°C")
            
            st.markdown("### 💧 Water & Humidity")
            humidity_range = crop_reqs.get('humidity_range', (0, 0))
            st.metric("Humidity Range", f"{humidity_range[0]}% - {humidity_range[1]}%")
            
            water_needs = crop_reqs.get('water_needs', 'unknown')
            water_icons = {
                'very_high': '💦💦💦💦',
                'high': '💦💦💦',
                'moderate': '💦💦',
                'low': '💦'
            }
            st.metric("Water Needs", f"{water_needs.title()} {water_icons.get(water_needs, '💦')}")
        
        with col2:
            st.markdown("### 📈 Growth Stage Analysis")
            # Current growth stage info
            sensitive_stages = crop_reqs.get('sensitive_stages', [])
            
            if growth_stage.lower() in [stage.lower() for stage in sensitive_stages]:
                st.error(f"⚠️ **{growth_stage}** is a sensitive stage for {crop_type}")
                st.markdown("**Monitor closely:** Weather conditions, pests, and diseases")
            else:
                st.success(f"✅ **{growth_stage}** stage is stable for {crop_type}")
                st.markdown("**Standard care:** Regular monitoring is sufficient")
            
            if sensitive_stages:
                st.markdown("### ⚠️ Critical Stages")
                for stage in sensitive_stages:
                    st.markdown(f"• **{stage.title()}** - Requires extra attention")
    else:
        st.error(f"❌ Growing information not available for {crop_type}")

with tab3:
    st.markdown("""
    <div class="chart-container">
        <h2>📊 Price Analytics & Forecasting</h2>
        <p>Historical trends and future price predictions</p>
    </div>
    """, unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("### 📊 30-Day Price History")
        historical_data = price_service.generate_historical_data(crop_type, 30)
        if historical_data is not None:
            st.line_chart(historical_data.set_index('Date')['Price'], height=400)
        else:
            st.info("📈 Historical data not available")

    with chart_col2:
        st.markdown("### 🔮 7-Day Price Forecast")
        predictions = price_service.predict_future_prices(crop_type, 7)
        if predictions is not None:
            st.line_chart(predictions.set_index('Date')['Predicted_Price'], height=400)
        else:
            st.info("🔮 Forecast data not available")
    
    # Additional analytics section
    st.markdown("### 📈 Market Insights")
    col1, col2, col3, col4 = st.columns(4)
    
    if current_price:
        with col1:
            st.metric("Today's Price", f"₹{current_price['current']:.2f}", f"{current_price['change']:+.1f}%")
        with col2:
            st.metric("Price Category", "Premium" if current_price['current'] > 100 else "Standard")
        with col3:
            st.metric("Market Status", "Bullish" if current_price['change'] > 0 else "Bearish")
        with col4:
            volatility = abs(current_price['change'])
            st.metric("Volatility", "High" if volatility > 3 else "Low", f"{volatility:.1f}%")

# Footer with enhanced styling
st.markdown(f"""
<div class="footer">
    <h4>🌾 AgroPrice Pro - Empowering Farmers with Data</h4>
    <p>Real-time market intelligence • Expert agricultural guidance • Maximized profits</p>
    <p><small>Last updated: {datetime.now().strftime("%d %B %Y at %H:%M IST")} | Serving farmers across India</small></p>
</div>
""", unsafe_allow_html=True)