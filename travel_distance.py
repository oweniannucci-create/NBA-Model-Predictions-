import googlemaps

cities_distances_dict={}

def get_distance_between_cities(origin_city, destination_city):
    # Replace 'YOUR_API_KEY' with your actual Google Maps API key
    gmaps = googlemaps.Client(key='AIzaSyAuuG32sSLWIWhH7-_XiU_Xx-NTw6KYmPw')

    if(origin_city+'-'+destination_city in cities_distances_dict):
        return cities_distances_dict[origin_city+'-'+destination_city]
    else:
        # Get distance matrix data
        distance_data = gmaps.distance_matrix(origin_city, destination_city)

        distance_value = distance_data['rows'][0]['elements'][0]['distance']['value'] # in meters
        cities_distances_dict[origin_city + '-' + destination_city]=distance_value
        return distance_value