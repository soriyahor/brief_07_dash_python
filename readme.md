#REAL ESTATE DASHBOARD FOR AGENCY CEO AND AGENT

Coding in python Dash a application for the real estate Director and agency responsible to best estimate price of a new house and make a fast check report to help decision.

---

# Table of Contents

1. [Overview](#overview)
2. [How to Run](#how-to-run)
3. [Different User Stories](#different-user-stories)
   - [1. Average income](#1-average-income)
   - [2. Transactions](#2-transactions)
   - [3. Number of sales par city](#3-number-of-sales-per-city)
   - [4. Small Apartment Transaction Count](#4-small-apartment-transaction-count)
   - [5. Count Small Apartments](#5-count-small-apartments)
   - [6. Property Piece Counts](#6-property-piece-counts)
   - [7. Average Price Per Square Meter](#7-average-price-per-square-meter)
   - [8. Sales by Department](#8-sales-by-department)
   - [9. Transactions in High-Income Cities](#9-transactions-in-high-income-cities)
4. [Notes](#notes)

---

## Overview

The application provides

1. access to real estate transaction data, allowing users to query various aspects such as average revenue, transaction counts, and specific data related to smaller apartments across different cities and years.
2. best estimated prices per square meter in IDF (Paris and neighbourgh) following a predictive model trained on a cleaned database

## How to Run

- Ensure FastAPI, dash, Uvicorn, requests are installed (pip install) / SQL / Python 3.12 or 3.117
- download : main.py / app.py / Chinook.db / configSQL.py / connecteurSQL.py / dashboard.py
- Run the server using 'python3 main.py' , assuming the script is named `main.py`
- Use VScode (via Anaconda recommanded)
- DataBase needed downloaded from
  https://www.kaggle.com/datasets/benoitfavier/immobilier-france/data extracted via Deabeaver more than 1,5Go
-

---

Main entries

- function to validate year entry : validate_year(year: str) => will return an error detail in case the year is not a 4 digit number
- function to validate an integer entry : validate_number(n: str) => will return an error detail in case the text indicates other than an integer
- function to validate an building type entry : validate_building_type(building_type: str) => will return an error detail in case the text is not 'appartement' or 'maison'
- under construction : function to validate the asked data exists in database => validate_existing_data => will return an error detail in case the text is not in the table(s)

---

## Different User Stories

---

Detailed user stories
https://docs.google.com/spreadsheets/d/110DFqhV0eNhR1mzBkRR5DD6Aey-lgXuTlf3VeSzWD58/edit#gid=0

    User story	                                                                                                            Tables concernées

1 En tant qu'Agent je veux pouvoir consulter le revenu fiscal moyen des foyers de ma ville foyers_fiscaux
2 En tant qu'Agent je veux consulter les 10 dernières transactions dans ma ville (Lyon) transactions
3 En tant qu'Agent je souhaite connaitre le nombre d'acquisitions dans ma ville (Paris) durant l'année 2022 transactions
4 En tant qu'Agent je souhaite connaitre le prix au m2 moyen pour les maisons vendues l'année 2022 transactions
5 En tant qu'Agent je souhaite connaitre le nombre d'acquisitions de studios dans ma ville (Rennes) durant l'année 2022 transactions
6 En tant qu'Agent je souhaite connaitre la répartition des appartements vendus (à Marseille) durant l'année 2022 en
fonction du nombre de pièces transactions
7 En tant qu'Agent je souhaite connaitre le prix au m2 moyen pour les maisons vendues à Avignon l'année 2022 transactions
8 En tant que CEO, je veux consulter le nombre de transactions (tout type confondu) par département, ordonnées par
ordre décroissant transactions
9 En tant que CEO je souhaite connaitre le nombre total de vente d'appartements en 2022 dans toutes les villes où le
revenu fiscal moyen en 2018 est supérieur à 70k transactions + foyers_fiscaux
10 En tant que CEO, je veux consulter le top 10 des villes les plus dynamiques en termes de transactions immobilières transactions
11 En tant que CEO, je veux accéder aux 10 villes avec un prix au m2 moyen le plus bas pour les appartements transactions
12 En tant que CEO, je veux accéder aux 10 villes avec un prix au m2 moyen le plus haut pour les maisons transactions

---

### 1. Average income

- **URL**: `/average_income_per_year_city/}`
- **Method**: `GET`
- **URL Params**:
  - `city=[string]` (required)
  - `year=[string]` (required in URL)
- **Success Response**: JSON object with average revenue.
- **Error Response**:
  - 400 Bad Request if year parameter is missing/invalid
  - 404 Not Found if no data is available
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/average_income_per_year_city/?year=2020&city=Montpellier`

### 2. Transactions

- **URL**: `/transactions_per_city/`
- **Method**: `GET`
- **Query Params**:
  - `city=[string]` (required)
  - `limit_number=[integer]` (required)
- **Success Response**: JSON object with a list of transactions.
- **Error Response**:
  - 400 Bad Request if cities parameter is missing
  - 404 Not Found if no transactions are found
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/transactions_per_city/?city=marigny&limit_number=2`

### 3. Number of sales par city

- **URL**: `/sales_per_city/`
- **Method**: `GET`
- **URL Params**:
  - `city=[string]` (required)
  - `year=[string]` (required)
- **Success Response**: JSON object with transaction count.
- **Error Response**:
  - 400 Bad Request if year is invalid
  - 404 Not Found if no data is found
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000//sales_per_city/?city=Paris&year=2018`

### 4. Small Apartment Transaction Count

- **URL**: `/small-apartment-transaction-count`
- **Method**: `GET`
- **Query Params**:
  - `city=[string]` (required)
  - `year=[integer]` (required)
- **Success Response**: JSON object with small apartment transaction count.
- **Error Response**:
  - 400 Bad Request if year is invalid
  - 404 Not Found if no data is found
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/small-apartment-transaction-count?city=Marseille&year=2021`

### 5. Count Small Apartments

- **URL**: `/count-small-apartments`
- **Method**: `GET`
- **Query Params**:
  - `city=[string]` (required)
  - `year=[integer]` (required)
- **Success Response**: JSON object with small apartment count.
- **Error Response**:
  - 400 Bad Request if year is invalid
  - 404 Not Found if no data is found
  - 500 Internal Server Error for other issues
- **Example**: `http://localhost:8000/count-small-apartments?city=Lyon&year=2023`

### 6. Property Piece Counts

- **URL**: `/piece-counts`
- **Method**: `GET`
- **No Query Params**
- **Success Response**: JSON object with the count of properties (apartments and houses) grouped by the number of pieces (rooms).
- **Error Response**:
  - 404 Not Found if no data is found
  - 500 Internal Server Error for database-related issues
- **Example**: `http://localhost:8000/piece-counts`

### 7. Average Price Per Square Meter

- **URL**: `/average-price-per-square-meter`
- **Method**: `GET`
- **Query Params**:
  - `city=[string]` (required)
  - `year=[integer]` (required)
  - `building_type=[string]` (required, e.g., 'Maison', 'Appartement')
- **Success Response**: JSON object with the price, habitable surface, and average price per square meter.
- **Error Response**:
  - 400 Bad Request if year is invalid or parameters are missing
  - 404 Not Found if no data is found
  - 500 Internal Server Error for database-related issues
- **Example**: `http://localhost:8000/average-price-per-square-meter?city=Avignon&year=2022&building_type=Maison`

### 8. Sales by Department

- **URL**: `/sales-by-department`
- **Method**: `GET`
- **No Query Params**
- **Success Response**: JSON object listing each department with its corresponding number of sales, ordered by the number of sales in descending order.
- **Error Response**:
  - 404 Not Found if no data is found
  - 500 Internal Server Error for database-related issues
- **Example**: `http://localhost:8000/sales-by-department`

### 9. Transactions in High-Income Cities

- **URL**: `/transactions-in-high-income-cities`
- **Method**: `GET`
- **Query Params**:
  - `city=[string]` (optional)
  - `minimum_income=[integer]` (optional, default is 10000)
- **Success Response**: JSON object listing each city with its corresponding number of real estate transactions in 2022, where the average fiscal revenue in 2018 was above the specified minimum income.
- **Error Response**:
  - 404 Not Found if no data is found
  - 500 Internal Server Error for database-related issues
- **Example**: `http://localhost:8000/transactions-in-high-income-cities?city=Paris&minimum_income=15000`

---

## Notes

- The database sample used is `Chinook.db`.
- Comprehensive error handling is implemented.
- The API is flexible for different cities and years.Projet Agence Immo is a Python and SQL library for dealing with data availible for a real estate agency. The objective is to create requests allowing a Director to take the right decisions where to implement his/her real estate agencies. These are the first requests to learn FastAPi

```


FastApi should be used as such.


## Usage
python VS Code Fast Api
internal usage only. for training only
```

Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

License
