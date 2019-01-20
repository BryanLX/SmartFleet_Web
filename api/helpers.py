import smartcar

def getAllVehicles(access):
    return smartcar.get_vehicle_ids(access['access_token'])['vehicles']

def getVehicleFromId(access, id):
    vehicle_ids = getAllVehicles(access)

    if id in vehicle_ids:
        vehicle = [smartcar.Vehicle(v, access['access_token']) for v in vehicle_ids if v == id][0]
        return vehicle
    return None

def getAddress(gmaps, latitude, longitude):
    result = gmaps.reverse_geocode((latitude, longitude))
    return result[0]['formatted_address']

def getDistance(gmaps, start, latitude, longitude):
    distance_matrix = gmaps.distance_matrix(start, (latitude, longitude))
    return distance_matrix['rows'][0]['elements'][0]['distance']

def getTime(gmaps, start, latitude, longitude):
    distance_matrix = gmaps.distance_matrix(start, (latitude, longitude))
    return distance_matrix['rows'][0]['elements'][0]['duration']

def getTimeAt(gmaps, start, latitude, longitude, start_time):
    distance_matrix = gmaps.distance_matrix(start, (latitude, longitude), departure_time=start_time)
    return distance_matrix['rows'][0]['elements'][0]['duration']
