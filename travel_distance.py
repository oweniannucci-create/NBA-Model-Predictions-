import googlemaps
import csv

def read_csv_to_dictionary(filename):
    """
    Reads a CSV file where each row is a comma-separated key-value pair
    and returns a dictionary.
    """
    data_dict = {}
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:  # Ensure the row has both a key and a value
                key, value = row
                data_dict[key.strip()] = value.strip() # Remove leading/trailing whitespace
            elif len(row) == 1 and row[0].strip(): # Handle cases with only a key and no value
                data_dict[row[0].strip()] = None # Assign None or an empty string as value
    return data_dict

cities_distances_dict=read_csv_to_dictionary('travel_distance.csv')
print(cities_distances_dict)

def get_distance_between_cities(origin_city, destination_city):
    # Replace 'YOUR_API_KEY' with your actual Google Maps API key
    print('finding distance from '+ origin_city + ' to '+ destination_city)
    gmaps = googlemaps.Client(key='AIzaSyAuuG32sSLWIWhH7-_XiU_Xx-NTw6KYmPw')

    if(origin_city+'-'+destination_city in cities_distances_dict):
        return cities_distances_dict[origin_city+'-'+destination_city]
    else:
        # Get distance matrix data
        distance_data = gmaps.distance_matrix(origin_city, destination_city)
        distance_value = distance_data['rows'][0]['elements'][0]['distance']['value'] # in meters
        print(distance_value)
        cities_distances_dict[origin_city + '-' + destination_city]=distance_value
        with open('travel_distance.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([origin_city+'-'+destination_city, distance_value])
        return distance_value

