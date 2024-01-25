import requests

ADDOK_URL = 'http://api-adresse.data.gouv.fr/search/'
# params = {
#     'q': '11 rue d haute ville, 75010 PARIS',
#     'limit': 5
# }

def create_long_lat(params):
    response = requests.get(ADDOK_URL, params)
    j = response.json()
    if len(j.get('features')) > 0:
        first_result = j.get('features')[0]
        lon, lat = first_result.get('geometry').get('coordinates')
        first_result_all_infos = { **first_result.get('properties'), **{"lon": lon, "lat": lat}}
        # print(first_result_all_infos)
        # for key, value in first_result_all_infos.items():
            # print(f"{key}: {value}")
        # Print only the postcode
        longitude = first_result_all_infos.get('lon')
        # if longitude:
        #     print(f"Longitude: {longitude}")
        # else:
        #     print("Longitude not available")
        # print(f"Latitude: {lat}, Longitude: {lon}")
        latitude = first_result_all_infos.get('lat')
        return longitude, latitude

    else:
        raise Exception

# print(create_long_lat({'q':'4 rue du carignan, 34830 clapiers'}))
# print(create_long_lat({'q':'4 rue du carignan, 34830 clapiers'})[0])
# print(create_long_lat({'q':'4 rue du carignan, 34830 clapiers'})[1])