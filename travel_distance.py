import googlemaps

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Define origin and destination cities
origin_city = 'Delhi'
destination_city = 'Mumbai'

# Get distance matrix data
distance_data = gmaps.distance_matrix(origin_city, destination_city)

# Extract distance and duration
distance_text = distance_data['rows'][0]['elements'][0]['distance']['text']
distance_value = distance_data['rows'][0]['elements'][0]['distance']['value'] # in meters
duration_text = distance_data['rows'][0]['elements'][0]['duration']['text']
duration_value = distance_data['rows'][0]['elements'][0]['duration']['value'] # in seconds

# Print the results
print(f"Distance between {origin_city} and {destination_city}: {distance_text} ({distance_value} meters)")
print(f"Driving duration: {duration_text} ({duration_value} seconds)")

# Example with coordinates
origin_coords = (12.9551779, 77.6910334) # Latitude, Longitude
destination_coords = (28.505278, 77.327774)

distance_data_coords = gmaps.distance_matrix(
    [f"{origin_coords[0]} {origin_coords[1]}"],
    [f"{destination_coords[0]} {destination_coords[1]}"]
)

distance_text_coords = distance_data_coords['rows'][0]['elements'][0]['distance']['text']
print(f"\nDistance between coordinates: {distance_text_coords}")