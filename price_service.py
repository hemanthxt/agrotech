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
            # Grains & Cereals
            "Wheat": "wheat", "Corn": "corn", "Rice": "rice", "Soybeans": "soybeans",
            "Barley": "barley", "Oats": "oats", "Millet": "millet", "Sorghum": "sorghum",
            "Quinoa": "quinoa", "Rye": "rye", "Buckwheat": "buckwheat", "Amaranth": "amaranth",
            "Pearl Millet": "pearl_millet", "Finger Millet": "finger_millet", "Foxtail Millet": "foxtail_millet",
            "Proso Millet": "proso_millet", "Triticale": "triticale", "Teff": "teff",
            
            # Fruits
            "Apple": "apple", "Mango": "mango", "Orange": "orange", "Grapes": "grapes",
            "Banana": "banana", "Coconut": "coconut", "Pineapple": "pineapple", "Papaya": "papaya",
            "Guava": "guava", "Pomegranate": "pomegranate", "Watermelon": "watermelon", "Muskmelon": "muskmelon",
            "Lemon": "lemon", "Lime": "lime", "Grapefruit": "grapefruit", "Avocado": "avocado",
            "Kiwi": "kiwi", "Dragon Fruit": "dragon_fruit", "Passion Fruit": "passion_fruit", "Fig": "fig",
            "Date Palm": "date_palm", "Jackfruit": "jackfruit", "Litchi": "litchi", "Rambutan": "rambutan",
            "Custard Apple": "custard_apple", "Strawberry": "strawberry", "Blueberry": "blueberry",
            "Blackberry": "blackberry", "Raspberry": "raspberry", "Gooseberry": "gooseberry",
            "Cherry": "cherry", "Plum": "plum", "Peach": "peach", "Apricot": "apricot", "Pear": "pear",
            
            # Vegetables
            "Tomatoes": "tomatoes", "Potatoes": "potatoes", "Lettuce": "lettuce", "Carrots": "carrots",
            "Onions": "onions", "Cucumbers": "cucumbers", "Peppers": "peppers", "Spinach": "spinach",
            "Broccoli": "broccoli", "Cabbage": "cabbage", "Beans": "beans", "Peas": "peas",
            "Squash": "squash", "Eggplant": "eggplant", "Radishes": "radishes", "Cauliflower": "cauliflower",
            "Okra": "okra", "Beetroot": "beetroot", "Turnip": "turnip", "Sweet Potato": "sweet_potato",
            "Pumpkin": "pumpkin", "Zucchini": "zucchini", "Bell Pepper": "bell_pepper", "Hot Pepper": "hot_pepper",
            "Kale": "kale", "Brussels Sprouts": "brussels_sprouts", "Asparagus": "asparagus", "Artichoke": "artichoke",
            "Celery": "celery", "Leek": "leek", "Fennel": "fennel", "Chard": "chard", "Arugula": "arugula",
            "Bok Choy": "bok_choy", "Watercress": "watercress", "Collard Greens": "collard_greens",
            "Mustard Greens": "mustard_greens", "Bitter Gourd": "bitter_gourd", "Bottle Gourd": "bottle_gourd",
            "Ridge Gourd": "ridge_gourd", "Snake Gourd": "snake_gourd", "Ash Gourd": "ash_gourd",
            "Ivy Gourd": "ivy_gourd", "Pointed Gourd": "pointed_gourd", "Drumstick": "drumstick",
            "Cluster Beans": "cluster_beans", "French Beans": "french_beans", "Broad Beans": "broad_beans",
            
            # Flowers
            "Sunflower": "sunflower", "Marigold": "marigold", "Rose": "rose", "Jasmine": "jasmine",
            "Chrysanthemum": "chrysanthemum", "Dahlia": "dahlia", "Carnation": "carnation", "Gladiolus": "gladiolus",
            "Tuberose": "tuberose", "Lily": "lily", "Lotus": "lotus", "Hibiscus": "hibiscus",
            "Ixora": "ixora", "Bougainvillea": "bougainvillea", "Petunia": "petunia", "Zinnia": "zinnia",
            "Cosmos": "cosmos", "Salvia": "salvia", "Celosia": "celosia", "Anthurium": "anthurium",
            "Orchid": "orchid", "Bird of Paradise": "bird_of_paradise", "Heliconia": "heliconia",
            "Gerbera": "gerbera", "Lavender": "lavender", "Calendula": "calendula", "Nasturtium": "nasturtium",
            "Pansy": "pansy", "Viola": "viola",
            
            # Herbs & Spices
            "Ginger": "ginger", "Garlic": "garlic", "Coriander": "coriander", "Mint": "mint",
            "Fenugreek": "fenugreek", "Mustard": "mustard", "Green Chili": "green_chili", "Turmeric": "turmeric",
            "Cumin": "cumin", "Cardamom": "cardamom", "Cinnamon": "cinnamon", "Clove": "clove",
            "Black Pepper": "black_pepper", "Nutmeg": "nutmeg", "Mace": "mace", "Star Anise": "star_anise",
            "Bay Leaf": "bay_leaf", "Curry Leaf": "curry_leaf", "Holy Basil": "holy_basil", "Sweet Basil": "sweet_basil",
            "Oregano": "oregano", "Thyme": "thyme", "Rosemary": "rosemary", "Sage": "sage",
            "Parsley": "parsley", "Cilantro": "cilantro", "Dill": "dill", "Chives": "chives",
            "Tarragon": "tarragon", "Marjoram": "marjoram", "Fennel Seeds": "fennel_seeds", "Carom Seeds": "carom_seeds",
            "Nigella Seeds": "nigella_seeds", "Poppy Seeds": "poppy_seeds", "Sesame Seeds": "sesame_seeds",
            "Vanilla": "vanilla", "Saffron": "saffron", "Asafoetida": "asafoetida", "Dried Red Chili": "dried_red_chili",
            
            # Cash Crops
            "Cotton": "cotton", "Sugarcane": "sugarcane", "Groundnut": "groundnut", "Sesame": "sesame",
            "Safflower": "safflower", "Castor": "castor", "Cashew": "cashew", "Tobacco": "tobacco",
            "Coffee": "coffee", "Tea": "tea", "Rubber": "rubber", "Coconut Palm": "coconut_palm",
            "Oil Palm": "oil_palm", "Jute": "jute", "Hemp": "hemp", "Flax": "flax", "Ramie": "ramie",
            "Sisal": "sisal", "Cocoa": "cocoa", "Black Pepper Vine": "black_pepper_vine", "Betel Nut": "betel_nut",
            "Cinnamon Tree": "cinnamon_tree", "Clove Tree": "clove_tree", "Nutmeg Tree": "nutmeg_tree",
            "Indigo": "indigo", "Henna": "henna", "Aloe Vera": "aloe_vera", "Stevia": "stevia", "Moringa": "moringa"
        }
        
        # Mock historical data for demonstration (in real implementation, this would come from APIs)
        # Prices in Indian Rupees (INR) per kilogram - based on realistic Indian market rates
        self.mock_prices = {
            # Grains & Cereals
            "wheat": {"current": 20.84, "unit": "INR/kg", "change": 2.3},
            "corn": {"current": 15.0, "unit": "INR/kg", "change": -1.2},
            "rice": {"current": 35.0, "unit": "INR/kg", "change": 5.1},
            "soybeans": {"current": 43.3, "unit": "INR/kg", "change": 3.8},
            "barley": {"current": 18.5, "unit": "INR/kg", "change": 1.7},
            "oats": {"current": 42.6, "unit": "INR/kg", "change": 2.1},
            "millet": {"current": 28.4, "unit": "INR/kg", "change": 3.4},
            "sorghum": {"current": 22.8, "unit": "INR/kg", "change": 1.9},
            "quinoa": {"current": 380.0, "unit": "INR/kg", "change": 4.5},
            "rye": {"current": 25.6, "unit": "INR/kg", "change": 1.2},
            "buckwheat": {"current": 55.8, "unit": "INR/kg", "change": 2.8},
            "amaranth": {"current": 125.4, "unit": "INR/kg", "change": 3.6},
            "pearl_millet": {"current": 32.5, "unit": "INR/kg", "change": 2.4},
            "finger_millet": {"current": 38.9, "unit": "INR/kg", "change": 1.8},
            "foxtail_millet": {"current": 45.2, "unit": "INR/kg", "change": 2.7},
            "proso_millet": {"current": 52.3, "unit": "INR/kg", "change": 3.1},
            "triticale": {"current": 24.7, "unit": "INR/kg", "change": 1.5},
            "teff": {"current": 195.8, "unit": "INR/kg", "change": 4.2},
            
            # Fruits
            "apple": {"current": 165.2, "unit": "INR/kg", "change": 1.9},
            "mango": {"current": 85.4, "unit": "INR/kg", "change": 3.6},
            "orange": {"current": 68.9, "unit": "INR/kg", "change": 1.7},
            "grapes": {"current": 125.8, "unit": "INR/kg", "change": 2.4},
            "banana": {"current": 45.8, "unit": "INR/kg", "change": 2.7},
            "coconut": {"current": 35.6, "unit": "INR/kg", "change": 2.8},
            "pineapple": {"current": 42.5, "unit": "INR/kg", "change": 3.2},
            "papaya": {"current": 38.7, "unit": "INR/kg", "change": 2.1},
            "guava": {"current": 55.3, "unit": "INR/kg", "change": 1.8},
            "pomegranate": {"current": 195.6, "unit": "INR/kg", "change": 4.5},
            "watermelon": {"current": 18.4, "unit": "INR/kg", "change": 2.9},
            "muskmelon": {"current": 32.8, "unit": "INR/kg", "change": 1.6},
            "lemon": {"current": 65.2, "unit": "INR/kg", "change": 3.8},
            "lime": {"current": 58.9, "unit": "INR/kg", "change": 2.7},
            "grapefruit": {"current": 85.4, "unit": "INR/kg", "change": 1.9},
            "avocado": {"current": 285.0, "unit": "INR/kg", "change": 4.1},
            "kiwi": {"current": 325.8, "unit": "INR/kg", "change": 3.5},
            "dragon_fruit": {"current": 450.0, "unit": "INR/kg", "change": 5.2},
            "passion_fruit": {"current": 380.6, "unit": "INR/kg", "change": 4.8},
            "fig": {"current": 245.3, "unit": "INR/kg", "change": 3.7},
            "date_palm": {"current": 185.7, "unit": "INR/kg", "change": 2.9},
            "jackfruit": {"current": 45.8, "unit": "INR/kg", "change": 2.4},
            "litchi": {"current": 125.9, "unit": "INR/kg", "change": 3.8},
            "rambutan": {"current": 285.4, "unit": "INR/kg", "change": 4.6},
            "custard_apple": {"current": 95.7, "unit": "INR/kg", "change": 2.8},
            "strawberry": {"current": 485.2, "unit": "INR/kg", "change": 5.4},
            "blueberry": {"current": 850.0, "unit": "INR/kg", "change": 6.2},
            "blackberry": {"current": 425.8, "unit": "INR/kg", "change": 4.9},
            "raspberry": {"current": 695.3, "unit": "INR/kg", "change": 5.8},
            "gooseberry": {"current": 165.4, "unit": "INR/kg", "change": 3.2},
            "cherry": {"current": 525.7, "unit": "INR/kg", "change": 4.7},
            "plum": {"current": 185.9, "unit": "INR/kg", "change": 3.4},
            "peach": {"current": 225.6, "unit": "INR/kg", "change": 3.9},
            "apricot": {"current": 295.8, "unit": "INR/kg", "change": 4.2},
            "pear": {"current": 145.3, "unit": "INR/kg", "change": 2.8},
            
            # Vegetables  
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
            "sweet_potato": {"current": 45.8, "unit": "INR/kg", "change": 2.3},
            "pumpkin": {"current": 25.4, "unit": "INR/kg", "change": 1.7},
            "zucchini": {"current": 68.9, "unit": "INR/kg", "change": 3.4},
            "bell_pepper": {"current": 185.6, "unit": "INR/kg", "change": 4.1},
            "hot_pepper": {"current": 225.8, "unit": "INR/kg", "change": 5.2},
            "kale": {"current": 125.4, "unit": "INR/kg", "change": 3.8},
            "brussels_sprouts": {"current": 195.7, "unit": "INR/kg", "change": 4.5},
            "asparagus": {"current": 485.2, "unit": "INR/kg", "change": 5.9},
            "artichoke": {"current": 325.6, "unit": "INR/kg", "change": 4.7},
            "celery": {"current": 85.9, "unit": "INR/kg", "change": 2.8},
            "leek": {"current": 145.3, "unit": "INR/kg", "change": 3.2},
            "fennel": {"current": 125.8, "unit": "INR/kg", "change": 2.9},
            "chard": {"current": 95.4, "unit": "INR/kg", "change": 3.6},
            "arugula": {"current": 185.7, "unit": "INR/kg", "change": 4.8},
            "bok_choy": {"current": 78.5, "unit": "INR/kg", "change": 2.4},
            "watercress": {"current": 245.8, "unit": "INR/kg", "change": 5.1},
            "collard_greens": {"current": 65.2, "unit": "INR/kg", "change": 2.7},
            "mustard_greens": {"current": 58.9, "unit": "INR/kg", "change": 2.3},
            "bitter_gourd": {"current": 95.6, "unit": "INR/kg", "change": 3.5},
            "bottle_gourd": {"current": 32.4, "unit": "INR/kg", "change": 1.8},
            "ridge_gourd": {"current": 48.7, "unit": "INR/kg", "change": 2.6},
            "snake_gourd": {"current": 42.5, "unit": "INR/kg", "change": 2.1},
            "ash_gourd": {"current": 28.3, "unit": "INR/kg", "change": 1.4},
            "ivy_gourd": {"current": 68.9, "unit": "INR/kg", "change": 3.2},
            "pointed_gourd": {"current": 75.6, "unit": "INR/kg", "change": 2.8},
            "drumstick": {"current": 185.4, "unit": "INR/kg", "change": 4.3},
            "cluster_beans": {"current": 125.8, "unit": "INR/kg", "change": 3.7},
            "french_beans": {"current": 145.2, "unit": "INR/kg", "change": 4.1},
            "broad_beans": {"current": 165.9, "unit": "INR/kg", "change": 3.9},
            
            # Flowers
            "sunflower": {"current": 78.3, "unit": "INR/kg", "change": 1.8},
            "marigold": {"current": 45.8, "unit": "INR/kg", "change": 3.2},
            "rose": {"current": 120.5, "unit": "INR/kg", "change": 2.8},
            "jasmine": {"current": 285.6, "unit": "INR/kg", "change": 5.4},
            "chrysanthemum": {"current": 95.4, "unit": "INR/kg", "change": 3.8},
            "dahlia": {"current": 165.2, "unit": "INR/kg", "change": 4.2},
            "carnation": {"current": 185.7, "unit": "INR/kg", "change": 3.9},
            "gladiolus": {"current": 125.8, "unit": "INR/kg", "change": 3.5},
            "tuberose": {"current": 225.4, "unit": "INR/kg", "change": 4.7},
            "lily": {"current": 385.9, "unit": "INR/kg", "change": 5.8},
            "lotus": {"current": 485.2, "unit": "INR/kg", "change": 6.2},
            "hibiscus": {"current": 68.5, "unit": "INR/kg", "change": 2.9},
            "ixora": {"current": 75.6, "unit": "INR/kg", "change": 3.1},
            "bougainvillea": {"current": 55.8, "unit": "INR/kg", "change": 2.4},
            "petunia": {"current": 145.3, "unit": "INR/kg", "change": 4.1},
            "zinnia": {"current": 85.7, "unit": "INR/kg", "change": 3.6},
            "cosmos": {"current": 65.2, "unit": "INR/kg", "change": 2.8},
            "salvia": {"current": 125.9, "unit": "INR/kg", "change": 3.9},
            "celosia": {"current": 95.4, "unit": "INR/kg", "change": 3.4},
            "anthurium": {"current": 485.6, "unit": "INR/kg", "change": 5.9},
            "orchid": {"current": 1250.0, "unit": "INR/kg", "change": 7.5},
            "bird_of_paradise": {"current": 685.4, "unit": "INR/kg", "change": 6.8},
            "heliconia": {"current": 385.7, "unit": "INR/kg", "change": 5.2},
            "gerbera": {"current": 285.8, "unit": "INR/kg", "change": 4.6},
            "lavender": {"current": 425.9, "unit": "INR/kg", "change": 5.4},
            "calendula": {"current": 165.2, "unit": "INR/kg", "change": 3.8},
            "nasturtium": {"current": 185.6, "unit": "INR/kg", "change": 4.2},
            "pansy": {"current": 225.4, "unit": "INR/kg", "change": 4.5},
            "viola": {"current": 195.8, "unit": "INR/kg", "change": 4.1},
            
            # Herbs & Spices
            "ginger": {"current": 245.8, "unit": "INR/kg", "change": 4.7},
            "garlic": {"current": 189.3, "unit": "INR/kg", "change": 2.2},
            "coriander": {"current": 125.6, "unit": "INR/kg", "change": 6.3},
            "mint": {"current": 98.7, "unit": "INR/kg", "change": 3.9},
            "fenugreek": {"current": 78.4, "unit": "INR/kg", "change": 1.8},
            "mustard": {"current": 65.2, "unit": "INR/kg", "change": 2.1},
            "green_chili": {"current": 158.3, "unit": "INR/kg", "change": 4.8},
            "turmeric": {"current": 210.5, "unit": "INR/kg", "change": 3.2},
            "cumin": {"current": 485.7, "unit": "INR/kg", "change": 5.8},
            "cardamom": {"current": 1850.0, "unit": "INR/kg", "change": 8.2},
            "cinnamon": {"current": 685.4, "unit": "INR/kg", "change": 6.5},
            "clove": {"current": 1250.8, "unit": "INR/kg", "change": 7.8},
            "black_pepper": {"current": 585.9, "unit": "INR/kg", "change": 6.2},
            "nutmeg": {"current": 985.4, "unit": "INR/kg", "change": 7.1},
            "mace": {"current": 1485.7, "unit": "INR/kg", "change": 8.5},
            "star_anise": {"current": 785.2, "unit": "INR/kg", "change": 6.8},
            "bay_leaf": {"current": 385.6, "unit": "INR/kg", "change": 5.4},
            "curry_leaf": {"current": 185.9, "unit": "INR/kg", "change": 4.2},
            "holy_basil": {"current": 125.4, "unit": "INR/kg", "change": 3.8},
            "sweet_basil": {"current": 145.8, "unit": "INR/kg", "change": 4.1},
            "oregano": {"current": 285.7, "unit": "INR/kg", "change": 5.2},
            "thyme": {"current": 485.2, "unit": "INR/kg", "change": 6.1},
            "rosemary": {"current": 385.9, "unit": "INR/kg", "change": 5.7},
            "sage": {"current": 425.6, "unit": "INR/kg", "change": 5.9},
            "parsley": {"current": 185.4, "unit": "INR/kg", "change": 4.3},
            "cilantro": {"current": 125.8, "unit": "INR/kg", "change": 3.9},
            "dill": {"current": 225.7, "unit": "INR/kg", "change": 4.8},
            "chives": {"current": 285.3, "unit": "INR/kg", "change": 5.1},
            "tarragon": {"current": 485.9, "unit": "INR/kg", "change": 6.4},
            "marjoram": {"current": 385.2, "unit": "INR/kg", "change": 5.6},
            "fennel_seeds": {"current": 185.6, "unit": "INR/kg", "change": 4.2},
            "carom_seeds": {"current": 285.4, "unit": "INR/kg", "change": 5.3},
            "nigella_seeds": {"current": 225.8, "unit": "INR/kg", "change": 4.7},
            "poppy_seeds": {"current": 385.7, "unit": "INR/kg", "change": 5.8},
            "sesame_seeds": {"current": 165.9, "unit": "INR/kg", "change": 3.9},
            "vanilla": {"current": 24500.0, "unit": "INR/kg", "change": 12.5},
            "saffron": {"current": 485000.0, "unit": "INR/kg", "change": 15.8},
            "asafoetida": {"current": 1850.6, "unit": "INR/kg", "change": 8.9},
            "dried_red_chili": {"current": 285.4, "unit": "INR/kg", "change": 5.2},
            
            # Cash Crops
            "cotton": {"current": 154.0, "unit": "INR/kg", "change": -2.5},
            "sugarcane": {"current": 3.5, "unit": "INR/kg", "change": 1.1},
            "groundnut": {"current": 98.5, "unit": "INR/kg", "change": 3.1},
            "sesame": {"current": 142.7, "unit": "INR/kg", "change": 2.9},
            "safflower": {"current": 89.2, "unit": "INR/kg", "change": 2.6},
            "castor": {"current": 67.4, "unit": "INR/kg", "change": 1.4},
            "cashew": {"current": 850.0, "unit": "INR/kg", "change": 4.2},
            "tobacco": {"current": 285.6, "unit": "INR/kg", "change": 3.8},
            "coffee": {"current": 485.9, "unit": "INR/kg", "change": 5.4},
            "tea": {"current": 385.2, "unit": "INR/kg", "change": 4.8},
            "rubber": {"current": 185.7, "unit": "INR/kg", "change": 3.2},
            "coconut_palm": {"current": 28.5, "unit": "INR/kg", "change": 2.1},
            "oil_palm": {"current": 45.8, "unit": "INR/kg", "change": 2.9},
            "jute": {"current": 68.4, "unit": "INR/kg", "change": 1.8},
            "hemp": {"current": 125.7, "unit": "INR/kg", "change": 3.4},
            "flax": {"current": 185.9, "unit": "INR/kg", "change": 4.1},
            "ramie": {"current": 225.6, "unit": "INR/kg", "change": 4.5},
            "sisal": {"current": 85.3, "unit": "INR/kg", "change": 2.7},
            "cocoa": {"current": 685.4, "unit": "INR/kg", "change": 6.8},
            "black_pepper_vine": {"current": 585.7, "unit": "INR/kg", "change": 6.2},
            "betel_nut": {"current": 385.9, "unit": "INR/kg", "change": 5.1},
            "cinnamon_tree": {"current": 785.6, "unit": "INR/kg", "change": 7.2},
            "clove_tree": {"current": 1285.4, "unit": "INR/kg", "change": 8.1},
            "nutmeg_tree": {"current": 1085.7, "unit": "INR/kg", "change": 7.6},
            "indigo": {"current": 485.8, "unit": "INR/kg", "change": 5.9},
            "henna": {"current": 285.3, "unit": "INR/kg", "change": 4.7},
            "aloe_vera": {"current": 125.9, "unit": "INR/kg", "change": 3.8},
            "stevia": {"current": 1285.6, "unit": "INR/kg", "change": 8.4},
            "moringa": {"current": 185.4, "unit": "INR/kg", "change": 4.2}
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