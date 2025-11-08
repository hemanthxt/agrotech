"""
Agricultural Assistant - Native Mobile App
Build this into APK for Android
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.list import MDList, OneLineListItem, ThreeLineListItem
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from datetime import datetime
import requests

# Import our modules
from weather_service import WeatherService
from price_service import PriceService
from financial_calculator import FinancialCalculator
from irrigation_calculator import IrrigationCalculator

class MainScreen(MDScreen):
    pass

class AgriAssistantApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weather_service = WeatherService()
        self.price_service = PriceService()
        self.financial_calc = FinancialCalculator()
        self.irrigation_calc = IrrigationCalculator()
        
        # Default values
        self.latitude = 28.6139
        self.longitude = 77.2090
        self.location_name = "New Delhi, India"
        self.crop_type = "Wheat"
        self.area_acres = 10.0
    
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        # Main layout
        layout = MDNavigationLayout()
        
        # Screen manager
        screen = MDScreen()
        
        # Top toolbar
        toolbar = MDTopAppBar(
            title="🌾 Agri Assistant",
            elevation=10,
            pos_hint={"top": 1},
            md_bg_color=self.theme_cls.primary_color,
            left_action_items=[["menu", lambda x: self.open_menu()]],
            right_action_items=[["weather", lambda x: self.show_weather()]]
        )
        
        # Main content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        content.size_hint_y = None
        content.bind(minimum_height=content.setter('height'))
        
        # Welcome card
        welcome = MDLabel(
            text=f"[b]Welcome to Agricultural Assistant![/b]\n\nLocation: {self.location_name}",
            markup=True,
            halign="center",
            size_hint_y=None,
            height=dp(80)
        )
        content.add_widget(welcome)
        
        # Crop selection
        crop_label = MDLabel(text="Select Crop:", size_hint_y=None, height=dp(40))
        content.add_widget(crop_label)
        
        self.crop_input = MDTextField(
            text=self.crop_type,
            hint_text="Enter crop name",
            mode="rectangle",
            size_hint_y=None,
            height=dp(50)
        )
        content.add_widget(self.crop_input)
        
        # Area input
        area_label = MDLabel(text="Farm Area (acres):", size_hint_y=None, height=dp(40))
        content.add_widget(area_label)
        
        self.area_input = MDTextField(
            text=str(self.area_acres),
            hint_text="Enter area",
            mode="rectangle",
            input_filter="float",
            size_hint_y=None,
            height=dp(50)
        )
        content.add_widget(self.area_input)
        
        # Action buttons
        btn_weather = MDRaisedButton(
            text="🌤️ Check Weather",
            size_hint_y=None,
            height=dp(50),
            on_release=self.show_weather
        )
        content.add_widget(btn_weather)
        
        btn_price = MDRaisedButton(
            text="💰 Check Prices",
            size_hint_y=None,
            height=dp(50),
            on_release=self.show_prices
        )
        content.add_widget(btn_price)
        
        btn_finance = MDRaisedButton(
            text="💵 Calculate Costs",
            size_hint_y=None,
            height=dp(50),
            on_release=self.show_finance
        )
        content.add_widget(btn_finance)
        
        btn_irrigation = MDRaisedButton(
            text="💧 Water Calculator",
            size_hint_y=None,
            height=dp(50),
            on_release=self.show_irrigation
        )
        content.add_widget(btn_irrigation)
        
        # Results display
        self.results_label = MDLabel(
            text="Select an option above to get started",
            markup=True,
            size_hint_y=None,
            height=dp(200)
        )
        content.add_widget(self.results_label)
        
        scroll.add_widget(content)
        screen.add_widget(toolbar)
        screen.add_widget(scroll)
        layout.add_widget(screen)
        
        return layout
    
    def open_menu(self):
        # Placeholder for menu
        pass
    
    def show_weather(self, *args):
        try:
            weather = self.weather_service.get_current_weather(self.latitude, self.longitude)
            if weather:
                result = f"""[b]Current Weather[/b]
                
🌡️ Temperature: {weather['temperature']}°C
💧 Humidity: {weather['humidity']}%
🌧️ Precipitation: {weather['precipitation']} mm
💨 Wind: {weather['wind_speed']} km/h

Location: {self.location_name}
Time: {datetime.now().strftime('%I:%M %p')}
"""
                self.results_label.text = result
            else:
                self.results_label.text = "[color=ff0000]Could not fetch weather data[/color]"
        except Exception as e:
            self.results_label.text = f"[color=ff0000]Error: {str(e)}[/color]"
    
    def show_prices(self, *args):
        try:
            crop = self.crop_input.text or self.crop_type
            price_data = self.price_service.get_current_price(crop)
            if price_data and 'current' in price_data:
                result = f"""[b]Price Information[/b]
                
Crop: {crop}
💰 Current Price: ₹{price_data['current']:.2f}/kg
📈 Change: {price_data['change']:+.1f}%

Updated: {datetime.now().strftime('%I:%M %p')}
"""
                self.results_label.text = result
            else:
                self.results_label.text = f"[color=ff0000]No price data for {crop}[/color]"
        except Exception as e:
            self.results_label.text = f"[color=ff0000]Error: {str(e)}[/color]"
    
    def show_finance(self, *args):
        try:
            crop = self.crop_input.text or self.crop_type
            area = float(self.area_input.text or self.area_acres)
            
            cost_data = self.financial_calc.calculate_total_cost(crop, area)
            
            result = f"""[b]Financial Summary[/b]
            
Crop: {crop}
Area: {area} acres

💰 Total Cost: ₹{cost_data['total_cost']:,.0f}
📊 Cost/Acre: ₹{cost_data['total_per_acre']:,.0f}

Breakdown:
• Seeds: ₹{cost_data['costs_per_acre'].get('seed', 0):,.0f}
• Fertilizer: ₹{cost_data['costs_per_acre'].get('fertilizer', 0):,.0f}
• Labor: ₹{cost_data['costs_per_acre'].get('labor', 0):,.0f}
• Irrigation: ₹{cost_data['costs_per_acre'].get('irrigation', 0):,.0f}
"""
            self.results_label.text = result
        except Exception as e:
            self.results_label.text = f"[color=ff0000]Error: {str(e)}[/color]"
    
    def show_irrigation(self, *args):
        try:
            crop = self.crop_input.text or self.crop_type
            area = float(self.area_input.text or self.area_acres)
            
            water_req = self.irrigation_calc.calculate_water_requirement(
                crop, area, "mid_season", 30, 60, 0
            )
            
            result = f"""[b]Water Requirements[/b]
            
Crop: {crop}
Area: {area} acres

💧 Daily Water: {water_req['daily_volume_liters']:,.0f} L
📊 Weekly: {water_req['weekly_volume_cubic_meters']:.1f} m³

Growth Stage: Mid Season
Temperature: 30°C
Humidity: 60%
"""
            self.results_label.text = result
        except Exception as e:
            self.results_label.text = f"[color=ff0000]Error: {str(e)}[/color]"

if __name__ == '__main__':
    AgriAssistantApp().run()
