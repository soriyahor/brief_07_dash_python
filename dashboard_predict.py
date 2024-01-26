from dash import Dash, html, dcc, dash_table, Output, Input, exceptions
import plotly.express as px
import pandas as pd
from predict.predict import prix_m2, prix_m2_two
from config_dashboard.gps import create_long_lat

app = Dash(__name__)



data = prix_m2( 0, 0)
# data = prix_m2("longitude", "latitude")
print(f"data : {data}")
# Convert the list of lists into a DataFrame
df = pd.DataFrame(data, columns=['longitude', 'latitude', 'prix_m2'])


table = dash_table.DataTable(id= 'data-table', data=df.to_dict('records'), columns=[{"name": i, "id": i} for i in df.columns])

map_figure = px.scatter_geo()

app.layout = html.Div(children=[
    html.H1(children='Dashboard', style={'textAlign':'center'}),

    html.Div(children='''
        Retourne le prix par m2
    '''),
    html.Br(),
    html.Label('Adresse:'),
    dcc.Input(id='adresse-input', type='text', value='11 rue d haute ville, 75010 PARIS' , style={'width': '20%'}) ,
    

    # html.Label('Longitude:'),
    # dcc.Input(id='longitude-input', type='number', value=0),

    # html.Label('Latitude:'),
    # dcc.Input(id='latitude-input', type='number', value=0),
    html.Button('Valider', id='validation-button'),

    html.Br(),
    html.Br(),
    dcc.Graph(id='map', figure=map_figure),

    table
])

# Mise à jour des données et du graphique en fonction de l'année sélectionnée
@app.callback(
    Output('data-table', 'data'),
    Output('map', 'figure'),
    Input('validation-button', 'n_clicks'),
    Input('adresse-input', 'value')
    # Input('longitude-input', 'value'),
    # Input('latitude-input', 'value')
)



def update_data(n_clicks,adresse):
    # print(f"longitude {longitude}")
    # print(f"n_clicks {n_clicks}")
    # print(f"latitude {latitude}")

    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        longitude = create_long_lat({'q':{adresse}})[0]
        print(f'longitude:{longitude}')
        latitude = create_long_lat({'q':{adresse}})[1]
        print(f'latitude:{latitude}')

        # longitude, latitude = create_long_lat({'q': {adresse}})
        # Mettez à jour les données en fonction de l'année sélectionnée
        data = prix_m2(longitude, latitude)
        # data = prix_m2("2.36", "48.38")
        print(f"data {data}")
        data2 = [[longitude, latitude, round(data.get('predicted_prix_m2'), 2)]]
        print(f"data2 {data2}")

        df = pd.DataFrame(data2, columns=['longitude', 'latitude', 'prix_m2'])
        print(f"df {df}")

        # Mettez à jour les données du tableau
        table_data = df.to_dict('records')

        map_figure = px.scatter_geo(df, lon='longitude', lat='latitude', text='prix_m2',
                                    projection='natural earth')
        map_figure.update_geos(
            center=dict(lon=2.0, lat=46.5),
            projection_scale=18,
            showcountries=True,
            countrycolor="darkgrey",
            showcoastlines=True,
            coastlinecolor="black"
        )

        return table_data, map_figure

if __name__ == '__main__':
    app.run(debug=True) 
