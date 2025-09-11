"""
Weather Outfit Assistant Lambda Function
Provides clothing recommendations based on weather conditions and user preferences
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Comprehensive closet catalog with 15+ items across 5 categories
CLOSET_CATALOG = CLOSET_CATALOG = [
    # Outerwear
    {
        "id": "jacket_001",
        "name": "Patagonia Waterproof Jacket",
        "category": "outerwear",
        "season": ["fall", "winter", "spring"],
        "weather_conditions": ["rainy", "windy", "cold"],
        "formality": "casual",
        "color": "navy_blue",
        "material": "waterproof_nylon",
        "last_worn": "2024-01-15",
        "available": True
    },
    {
        "id": "coat_001",
        "name": "Wool Business Coat",
        "category": "outerwear",
        "season": ["fall", "winter"],
        "weather_conditions": ["cold", "windy"],
        "formality": "business_formal",
        "color": "charcoal_gray",
        "material": "wool",
        "last_worn": "2024-01-10",
        "available": True
    },
    # Tops
    {
        "id": "shirt_001",
        "name": "White Oxford Shirt",
        "category": "tops",
        "season": ["spring", "summer", "fall"],
        "weather_conditions": ["sunny", "mild", "warm"],
        "formality": "business_formal",
        "color": "white",
        "material": "cotton",
        "last_worn": "2024-01-18",
        "available": True
    },
    {
        "id": "sweater_001",
        "name": "Merino Wool Sweater",
        "category": "tops",
        "season": ["fall", "winter"],
        "weather_conditions": ["cold", "cool"],
        "formality": "business_casual",
        "color": "forest_green",
        "material": "merino_wool",
        "last_worn": "2024-01-12",
        "available": True
    },
    {
        "id": "tshirt_001",
        "name": "Graphic Cotton T-Shirt",
        "category": "tops",
        "season": ["spring", "summer"],
        "weather_conditions": ["sunny", "warm"],
        "formality": "casual",
        "color": "black",
        "material": "cotton",
        "last_worn": "2024-01-20",
        "available": True
    },
    {
        "id": "polo_001",
        "name": "Navy Blue Polo Shirt",
        "category": "tops",
        "season": ["spring", "summer"],
        "weather_conditions": ["mild", "warm"],
        "formality": "business_casual",
        "color": "navy_blue",
        "material": "cotton",
        "last_worn": "2024-01-17",
        "available": True
    },
    # Bottoms
    {
        "id": "jeans_001",
        "name": "Dark Wash Jeans",
        "category": "bottoms",
        "season": ["spring", "fall", "winter"],
        "weather_conditions": ["mild", "cool", "cold"],
        "formality": "casual",
        "color": "dark_blue",
        "material": "denim",
        "last_worn": "2024-01-21",
        "available": True
    },
    {
        "id": "trousers_001",
        "name": "Wool Dress Trousers",
        "category": "bottoms",
        "season": ["fall", "winter", "spring"],
        "weather_conditions": ["mild", "cool", "cold"],
        "formality": "business_formal",
        "color": "charcoal_gray",
        "material": "wool",
        "last_worn": "2024-01-14",
        "available": True
    },
    {
        "id": "shorts_001",
        "name": "Khaki Chino Shorts",
        "category": "bottoms",
        "season": ["summer"],
        "weather_conditions": ["sunny", "warm"],
        "formality": "casual",
        "color": "khaki",
        "material": "cotton",
        "last_worn": "2024-01-22",
        "available": True
    },
    # Footwear
    {
        "id": "sneakers_001",
        "name": "White Running Shoes",
        "category": "footwear",
        "season": ["spring", "summer", "fall"],
        "weather_conditions": ["sunny", "mild", "warm"],
        "formality": "casual",
        "color": "white",
        "material": "synthetic",
        "last_worn": "2024-01-23",
        "available": True
    },
    {
        "id": "boots_001",
        "name": "Leather Ankle Boots",
        "category": "footwear",
        "season": ["fall", "winter", "spring"],
        "weather_conditions": ["cool", "cold", "rainy"],
        "formality": "business_casual",
        "color": "brown",
        "material": "leather",
        "last_worn": "2024-01-13",
        "available": True
    },
    {
        "id": "dress_shoes_001",
        "name": "Black Leather Oxford Shoes",
        "category": "footwear",
        "season": ["fall", "winter", "spring"],
        "weather_conditions": ["mild", "cool"],
        "formality": "business_formal",
        "color": "black",
        "material": "leather",
        "last_worn": "2024-01-11",
        "available": True
    },
    # Accessories
    {
        "id": "scarf_001",
        "name": "Cashmere Winter Scarf",
        "category": "accessories",
        "season": ["fall", "winter"],
        "weather_conditions": ["cold", "windy"],
        "formality": "business_casual",
        "color": "gray",
        "material": "cashmere",
        "last_worn": "2024-01-09",
        "available": True
    },
    {
        "id": "belt_001",
        "name": "Brown Leather Belt",
        "category": "accessories",
        "season": ["all"],
        "weather_conditions": ["all"],
        "formality": "business_casual",
        "color": "brown",
        "material": "leather",
        "last_worn": "2024-01-16",
        "available": True
    },
    {
        "id": "cap_001",
        "name": "Baseball Cap",
        "category": "accessories",
        "season": ["spring", "summer"],
        "weather_conditions": ["sunny", "warm"],
        "formality": "casual",
        "color": "navy_blue",
        "material": "cotton",
        "last_worn": "2024-01-19",
        "available": True
    },
    # Summer Tops
    {
        "id": "linen_shirt_001",
        "name": "Beige Linen Short Sleeve Shirt",
        "category": "tops",
        "season": ["summer"],
        "weather_conditions": ["sunny", "hot", "humid"],
        "formality": "business_casual",
        "color": "beige",
        "material": "linen",
        "last_worn": "2024-07-05",
        "available": True
    },
    {
        "id": "hawaiian_001",
        "name": "Floral Hawaiian Shirt",
        "category": "tops",
        "season": ["summer"],
        "weather_conditions": ["sunny", "hot"],
        "formality": "casual",
        "color": "multi_color",
        "material": "cotton",
        "last_worn": "2024-07-08",
        "available": True
    },
    {
        "id": "tanktop_001",
        "name": "Black Cotton Tank Top",
        "category": "tops",
        "season": ["summer"],
        "weather_conditions": ["sunny", "hot"],
        "formality": "casual",
        "color": "black",
        "material": "cotton",
        "last_worn": "2024-07-12",
        "available": True
    },

    # Summer Bottoms
    {
        "id": "linen_pants_001",
        "name": "Lightweight Linen Pants",
        "category": "bottoms",
        "season": ["summer"],
        "weather_conditions": ["hot", "humid"],
        "formality": "business_casual",
        "color": "light_gray",
        "material": "linen",
        "last_worn": "2024-07-10",
        "available": True
    },
    {
        "id": "swimshorts_001",
        "name": "Navy Blue Swim Shorts",
        "category": "bottoms",
        "season": ["summer"],
        "weather_conditions": ["sunny", "hot"],
        "formality": "casual",
        "color": "navy_blue",
        "material": "polyester",
        "last_worn": "2024-07-15",
        "available": True
    },

    # Summer Footwear
    {
        "id": "sandals_001",
        "name": "Leather Strap Sandals",
        "category": "footwear",
        "season": ["summer"],
        "weather_conditions": ["sunny", "hot"],
        "formality": "casual",
        "color": "brown",
        "material": "leather",
        "last_worn": "2024-07-09",
        "available": True
    },
    {
        "id": "loafers_001",
        "name": "Beige Suede Loafers",
        "category": "footwear",
        "season": ["summer"],
        "weather_conditions": ["hot", "mild"],
        "formality": "business_casual",
        "color": "beige",
        "material": "suede",
        "last_worn": "2024-07-11",
        "available": True
    },

    # Summer Accessories
    {
        "id": "sunglasses_001",
        "name": "Polarized Sunglasses",
        "category": "accessories",
        "season": ["summer"],
        "weather_conditions": ["sunny"],
        "formality": "casual",
        "color": "black",
        "material": "plastic",
        "last_worn": "2024-07-07",
        "available": True
    },
    {
        "id": "hat_001",
        "name": "Straw Sun Hat",
        "category": "accessories",
        "season": ["summer"],
        "weather_conditions": ["sunny", "hot"],
        "formality": "casual",
        "color": "beige",
        "material": "straw",
        "last_worn": "2024-07-06",
        "available": True
    }
]

def filter_closet_items(filters: Optional[Dict] = None) -> List[Dict]:
    """Filter closet items based on provided criteria"""
    if not filters:
        return CLOSET_CATALOG
    
    filtered_items = CLOSET_CATALOG.copy()
    
    # Apply filters
    if filters.get('category'):
        filtered_items = [item for item in filtered_items if item['category'] == filters['category']]
    
    if filters.get('season'):
        filtered_items = [item for item in filtered_items if filters['season'] in item['season']]
    
    if filters.get('formality'):
        filtered_items = [item for item in filtered_items if item['formality'] == filters['formality']]
    
    if filters.get('available') is not None:
        filtered_items = [item for item in filtered_items if item['available'] == filters['available']]
    
    return filtered_items

def generate_outfit_recommendation(
    user_id: str = "user123",
    weather_conditions: Optional[Dict] = None,
    occasion: str = "casual",
    preferences: Optional[Dict] = None
) -> Dict:
    """Generate outfit recommendation based on weather and preferences"""
    
    # Default weather if not provided
    if not weather_conditions:
        weather_conditions = {
            "temperature": 20,
            "description": "partly cloudy",
            "humidity": 60
        }
    
    # Determine formality level
    formality_map = {
        "casual": "casual",
        "work": "business_casual",
        "business": "business_formal",
        "formal": "business_formal"
    }
    formality = formality_map.get(occasion.lower(), "casual")
    
    # Build recommendation
    recommendation = {
        "user_id": user_id,
        "weather_analysis": {
            "temperature": weather_conditions.get("temperature"),
            "formality": formality
        },
        "outfit_pieces": {},
        "styling_advice": []
    }
    
    # Select outfit pieces by category
    categories = ["outerwear", "tops", "bottoms", "footwear"]
    
    for category in categories:
        # Filter items for this category
        category_items = filter_closet_items({
            "category": category,
            "formality": formality,
            "available": True
        })
        
        # If no exact matches, broaden the search
        if not category_items:
            category_items = filter_closet_items({
                "category": category,
                "available": True
            })
        
        # Select best item (least recently worn)
        if category_items:
            category_items.sort(key=lambda x: x['last_worn'])
            selected_item = category_items[0]
            
            recommendation["outfit_pieces"][category] = {
                "item": selected_item,
                "reason": f"Selected for {formality} {occasion}"
            }
    
    # Add styling advice based on weather
    temp = weather_conditions.get("temperature", 20)
    if temp < 10:
        recommendation["styling_advice"].append("Layer clothing for warmth")
    elif temp > 25:
        recommendation["styling_advice"].append("Choose breathable fabrics")
    
    return recommendation

def lambda_handler(event, context):
    """Main Lambda handler"""
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Parse the request
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        action = body.get('action', 'get_closet_catalog')
        
        if action == 'get_closet_catalog':
            # Get closet catalog with optional filters
            user_id = body.get('user_id', 'user123')
            filters = body.get('filters', {})
            
            filtered_items = filter_closet_items(filters)
            
            response = {
                "user_id": user_id,
                "total_items": len(filtered_items),
                "filters_applied": filters,
                "items": filtered_items
            }
            
        elif action == 'generate_outfit_recommendation':
            # Generate outfit recommendation
            user_id = body.get('user_id', 'user123')
            weather_conditions = body.get('weather_conditions', {})
            occasion = body.get('occasion', 'casual')
            preferences = body.get('preferences', {})
            
            response = generate_outfit_recommendation(
                user_id=user_id,
                weather_conditions=weather_conditions,
                occasion=occasion,
                preferences=preferences
            )
            
        else:
            raise ValueError(f"Unknown action: {action}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response, default=str)
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }