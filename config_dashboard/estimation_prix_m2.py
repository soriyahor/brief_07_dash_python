import requests

racine_api = 'http://127.0.0.1:8000'

def estimation_prix_m2(longitude, latitude):
    try:
        response = requests.post(racine_api + '/prix_m2/', params={'longitude': longitude, 'latitude': latitude})
        data = response.json()
        return data
    except Exception as e:
        print(str(e))

print(estimation_prix_m2('2.349933', '48.872006'))


