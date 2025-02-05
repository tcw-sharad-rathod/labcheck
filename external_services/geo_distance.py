# Defines functions for geolocation distance calculation

from geopy.distance import geodesic

# def calculate_distance(coord1, coord2):
#     return geodesic(coord1, coord2).km




import math

def calculate_distance(loc1, loc2):
    if not loc1 or not loc2 or len(loc1) != 2 or len(loc2) != 2:
        return float('inf')
    
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(float, loc1 + loc2)
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def calculate_distance123(loc1, loc2):
    """Haversine formula to calculate the distance between two lat/lon points."""
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(float, loc1 + loc2)
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  # Distance in km