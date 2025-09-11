# Agricultural Weather Monitor

## Overview

This is a Streamlit-based web application that provides real-time weather monitoring and crop-specific recommendations for farmers. The application integrates weather data from the Open-Meteo API with agricultural knowledge to help farmers make informed decisions about their crops based on current and forecasted weather conditions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid development of data applications
- **Layout**: Wide layout with expandable sidebar for user inputs
- **Visualization**: Plotly for interactive weather charts and graphs
- **Data Display**: Pandas DataFrames for structured data presentation
- **UI Components**: Number inputs, select boxes, and text inputs for farm location and crop selection

### Backend Architecture
- **Modular Design**: Separated into distinct service modules for maintainability
  - `weather_service.py`: Handles all weather data fetching and processing
  - `crop_recommendations.py`: Manages crop-specific agricultural recommendations
  - `utils.py`: Contains utility functions for data formatting and calculations
- **Caching Strategy**: Streamlit's built-in caching with 5-minute TTL to optimize API calls
- **Error Handling**: Graceful error handling with user-friendly error messages

### Data Processing
- **Weather Data**: Real-time current conditions and multi-day forecasts
- **Agricultural Intelligence**: Crop-specific requirements database with temperature ranges, humidity needs, and growth stage sensitivity
- **Utility Calculations**: Heat index calculations for farmer safety and UV risk assessments

### Service Integration Pattern
- **Weather Service**: Encapsulates Open-Meteo API interactions with proper error handling and data transformation
- **Crop Recommendations**: Provides intelligent recommendations based on weather conditions and crop requirements
- **Utility Functions**: Reusable functions for temperature/precipitation formatting and weather condition mapping

## External Dependencies

### Weather Data API
- **Open-Meteo API**: Free weather API providing current conditions and forecasts
  - Endpoints: Current weather and daily forecast
  - Data: Temperature, humidity, precipitation, wind speed/direction
  - No API key required, with built-in rate limiting considerations

### Python Libraries
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization (graph_objects and express)
- **Requests**: HTTP client for API communications

### Data Sources
- **Crop Database**: Internal crop requirements database with agricultural parameters for 10+ crop types including optimal temperature ranges, humidity requirements, and water needs
- **Weather Icons**: Emoji-based weather condition representation system