

# Function to calculate the distance between two locations using the Haversine formula
# The function takes two arguments, loc1 and loc2, which are lists or tuples containing the latitude and longitude of the two locations
# The function returns the distance between the two locations in kilometers

import math

def calculate_distance(loc1, loc2):
    if loc1 is None or loc2 is None:
        return float('inf')  # Return a large value instead of None

    if not isinstance(loc1, (list, tuple)) or not isinstance(loc2, (list, tuple)) or len(loc1) != 2 or len(loc2) != 2:
        return float('inf')

    if any(x is None for x in loc1 + loc2):
        return float('inf')

    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(float, loc1 + loc2)
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    print("result", R * c)
    return R * c

# # Example usage
# loc1 = (40.7128, -74.0060)  # New York City

# loc2 = (37.7749, -122.4194)  # San Francisco

# distance = calculate_distance(loc1, loc2)

# print(f"The distance between New York City and San Francisco is {distance:.2f} kilometers.")  # Output: The distance between New York City and San Francisco is 1,699.41 kilometers.
