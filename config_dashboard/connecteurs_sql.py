import requests
import time
from config_dashboard.config_sql import *


#definir une méthode get
def get(endpoint: str, parameters: dict):
    start = time.time()
    res =requests.get(racine_api + endpoint, parameters)
    end = time.time()
    print("Temps de request", end - start)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception('ERROR: ' + str(res.content))


def revenu_fiscal (city: str, year: int =None):
    try:
        return get(end1, {"city": city, "year": year})
    except Exception as e:
        print(str(e))

def last_transaction (city: str, limit):
    try:
        return get(end2, {"city": city, "limit": limit})
    except Exception as e:
        print(str(e))

def acquisition_number (city: str, year, nb_piece: str =""):
    try:
        return get(end3, {"city": city, "year": year, "nb_piece": nb_piece})
    except Exception as e:
        print(str(e))

def average_price (type_bat, year, city: str=""):
    try:
        return get(end4, {"type_batiment": type_bat, "year": year,"city": city})
    except Exception as e:
        print(str(e))

def repartition (type_bat, city, year):
    try:
        return get(end5, {"type_batiment": type_bat,"city": city, "year": year })
    except Exception as e:
        print(str(e))

def departement (year: int=None):
    try:
        return get(end6, {"year": year})
    except Exception as e:
        print(str(e))

def immo_et_revenufisc (type_bat, year, fiscal_year, revenu_fiscal_moy):
    try:
        return get(end7, {"type_batiment": type_bat, "year": year,"fiscal_year": fiscal_year, "revenu_fiscal_moyen": revenu_fiscal_moy})
    except Exception as e:
        print(str(e))

def dynamism (limit, year: int =None):
    try:
        return get(end8, {"limit_top": limit, "year": year})
    except Exception as e:
        print(str(e))

def price_limit(type_bat, asc, limit):
    try:
        return get(end8, {"type_batiment": type_bat, "ascendant": asc, "limit_top": limit})
    except Exception as e:
        print(str(e))

# print("Le revenu fiscal moyen est:")
# print(revenu_fiscal('Montpellier', 2020))

# print ("les n dernières transactions:")
# print(last_transaction('montpellier', 2))

# print ("Nombres d'acquisitions:")
# print(acquisition_number('Montpellier', 2020, 2))

# print ("Prix moyen:")
# print(average_price('Maison', 2020, 'Montpellier'))

# print ("Repartition:")
# print(repartition('Maison', 'Montpellier', 2020))

# print ("Top departement:")
# print(departement(2020))

# print ("Retourne le nombre de transactions (tout type confondu) par département, ordonnées par ordre décroissant:")
# print(immo_et_revenufisc('Maison', 2022, 2018, 70000))

#print ("Retourne le top 10 des villes les plus dynamiques en termes de transactions immobilières:")
#print(dynamism(10, 2022))

#print("Retourne le top + ou - des prix au m2 des Maisons ou Appartements")
#print(price_limit('Maison', False, 5))