#REAL ESTATE LAST OUTPUT FOR AGENCY

Coding in python Dash an application for the real estate Director and agency responsible to best estimate price of a new house and make a fast check report to help decision.

***

# Table of Contents
1. [Overview](#overview)
2. [How to Run](#how-to-run)
3. [Different views](#different-views)
   - [1. CEO](#1-ceo)
   - [2. Real Estate Agent](#2-real-estate-agent)
4. [Notes](#notes)

***

## Overview

The application provides 
1. access to real estate transactions data, graphs to view number of transactions per department per cities.
2. best estimated prices per square meter in IDF (Paris and neighbourgh) following a predictive model trained on a cleaned database

## How to Run

- Ensure FastAPI, dash, Uvicorn, requests, pickle are installed (pip install) / SQL / Python 3.12 or 3.117
- download : all files and repositories from github
- Use VScode (via Anaconda recommanded)
- DataBase needed downloaded from
https://www.kaggle.com/datasets/benoitfavier/immobilier-france/data extracted via Deabeaver more than 1,5Go => named 'chinook.db'
- models in Pickle have been generated with GridSearch on this database and results of the training are named : 'optimal_rfr_model_paris.pkl' and 'optimal_rfr_model_idf.pkl'
1. Run the file named : requete_sql.py in 'requete_sql' with 'python3 requete_sql.py' based on chinook.db datas
2. Run the file named : predict.py in 'requete_sqlpredict' with 'python3 predict.py' based on 'optimal_rfr_model_paris.pkl' and 'optimal_rfr_model_idf.pkl' datas
3. Run the file named : dashboard.py with 'python3 dashboard.py' based on the 2 last queries

***

## Different views

You will access to the main dashboard page with a firstdefault view on CEO
`http://127.0.0.1:8050/`

***
### 1. CEO
- **URL**: `http://127.0.0.1:8050/`
- **Method**: `POST` & SQL
- **URL Params**: 
  - `city=[string]` (required)
  - `year=[string]` (required in URL)
- **Success Response**: histogram and table.
- **Error Response**: 
  - 400 Bad Request if year parameter is missing/invalid
  - 404 Not Found if no data is available
  - 500 Internal Server Error for other issues
- **Example**: `http://127.0.0.1:8050/`

### 2. Real Estate Agent
- **URL**: `http://127.0.0.1:8050/`
- **Method**: `POST & PREDICT`
- **Query Params**: 
  - `adresse=[string]` (required and limited to Ile de France only)
- **Success Response**: map and table with price per square meter indicated.
- **Error Response**: 
  - 400 Bad Request if adress is missing
  - 404 Not Found if no transactions are found
  - 500 Internal Server Error for other issues
- **Example**: `http://127.0.0.1:8050/`


***

## Notes

- The database sample used is `Chinook.db` and has been cleaned and reworked with a new column named "Year" on the transaction table.
- The models have been trained on this transaction table and the chosen model is the Random Forest one with 2 parameters : longitude and latitude. 
To help the end user real estate agent, we have introduced a function based on open data API from French Government to get coordinates from adress (this function is defined in `gps.py``in config_dashboard repository)


```

## Usage

internal usage only. for training only
```

Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

License