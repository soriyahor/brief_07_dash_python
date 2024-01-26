# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, callback, Output, Input, dash_table, exceptions
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from config_dashboard.gps import create_long_lat
from config_dashboard.connecteurs_sql import dynamism, departement
from config_dashboard.estimation_prix_m2 import estimation_prix_m2

app = Dash(__name__)

#Layout principal

app.layout = html.Div([
    html.H1(children='Bienvenue FACILIMMOUETTE', style={'textAlign':'center'}),
    dcc.Dropdown(id='ceo-vs-agent-dropdown', options=[{'label': r, 'value': r} for r in ['CEO', 'AGENT']],
        value=None,  # Aucune rôle sélectionné par défaut
        multi=False,
        placeholder="Sélectionnez un rôle",
    ),
    html.Div(id='ceo-or-agent-div')
    ])

@app.callback(Output('ceo-or-agent-div', 'children'),
              Input('ceo-vs-agent-dropdown', 'value'))
def update_ceo_agent_div(value: str):
    if value == 'CEO':
        return ceo_layout
    elif value == 'AGENT':
        return agent_layout
    else:
        None

# liste des années uniques pour la création du menu déroulant
years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
print("Chargement du dataframe1, merci de patienter max 1min")
df1 = pd.DataFrame(dynamism(10,), columns=["Ville", "nb transac"]) #pour accelerer possible de  mettre 2022 en paramètre de dynamism, à enlever
fig1 = px.bar(df1, x="Ville", y="nb transac")
table1 = dash_table.DataTable(id= 'data-table1', data=df1.to_dict('records'), columns=[{"name": col, "id": col} for col in df1.columns])

print("Chargement du dataframe2, merci de patienter max 1min")
df2 = pd.DataFrame(departement(), columns=['departement', 'nb'])
fig2 = px.bar(df2, x='departement', y='nb')
table2 = dash_table.DataTable(id= 'data-table2', data=df2.to_dict('records'), columns=[{"name": i, "id": i} for i in df2.columns])

#Layout CEO
ceo_layout = dbc.Container(
    [
        html.H2(children='Top 10 des villes les plus dynamiques en termes de transactions immobilières', style={'textAlign': 'center'}),
        html.Div(children='''Possible de filtrer sur une année anterieure:'''),
        dcc.Dropdown(
            id='dropdown-year1',
            options=[{'label': year, 'value': year} for year in years],
            value=max(years),  # Année la plus récente sélectionnée par défaut
            multi=False,
            placeholder="Sélectionnez une année",
            style={'width': '50%'}  # Ajustez la largeur 
        ),
        dcc.Loading(
            id="loading-data",
            type="circle",
            children = [
                html.Div(
                    [
                        dcc.Graph(id='graph-content1', figure=fig1, style={'display': 'inline-block', 'width': '49%'}),
                        html.Div(table1, style={'display': 'inline-block', 'width': '49%', 'padding-left': '20px'}),  # Ajout de padding
                    ],
                    style={'display': 'flex'},
                ),
            ]
        ),
        html.H2(children='Top departement', style={'textAlign': 'center'}),
        html.Div(children='''Possible de filtrer sur une année anterieure:'''),
        dcc.Dropdown(
            id='dropdown-year2',
            options=[{'label': year, 'value': year} for year in years],
            value=max(years),  # Année la plus récente sélectionnée par défaut
            multi=False,
            placeholder="Sélectionnez une année",
            style={'width': '50%'}  # Ajustez la largeur 
        ),
        dcc.Loading(
            id="loading-data",
            type="circle",
            children = [
                html.Div(
                    [
                        dcc.Graph(id='graph-content2', figure=fig2, style={'display': 'inline-block', 'width': '49%'}),
                        html.Div(table2, style={'display': 'inline-block', 'width': '49%', 'padding-left': '20px'}),  # Ajout de padding
                    ],
                    style={'display': 'flex'},
                ),
            ]
        )
    ],
)


@app.callback(
    Output('graph-content1', 'figure'),
    Output('data-table1', 'data'),
    Input('dropdown-year1', 'value')
)
def update_graph(selected_year):
    if selected_year is None:
        df_updated = pd.DataFrame(dynamism(10), columns=["Ville", "nb transac"])
    else:
        df_updated = pd.DataFrame(dynamism(10, selected_year), columns=["Ville", "nb transac"])
   
    fig_updated = px.bar(df_updated, x="Ville", y="nb transac")
    print("updating data")
    return fig_updated, df_updated.to_dict('records')


@app.callback(
    Output('graph-content2', 'figure'),
    Output('data-table2', 'data'),
    Input('dropdown-year2', 'value')
)
def update_graph2(selected_year):
    if selected_year is None:
        df2_updated = pd.DataFrame(departement(), columns=['departement', 'nb'])
    else:
        df2_updated = pd.DataFrame(departement(selected_year), columns=['departement', 'nb'])
   
    fig2_updated = px.bar(df2_updated, x='departement', y='nb')
    return fig2_updated, df2_updated.to_dict('records')

# agent

data = estimation_prix_m2( 0, 0)
df = pd.DataFrame(data, columns=['longitude', 'latitude', 'prix_m2'])
table = dash_table.DataTable(id= 'data-table', data=df.to_dict('records'), columns=[{"name": i, "id": i} for i in df.columns])
map_figure = px.scatter_geo()

# layout agent
agent_layout = html.Div(children=[
    html.H1(children='Estimation du prix au m² de la ville de Paris', style={'textAlign':'center'}),
    html.Div(children='''
        Retourne le prix par m2
    '''),
    html.Br(),
    html.Label('Adresse:'),
    dcc.Input(id='adresse-input', type='text', value='11 rue d haute ville, 75010 PARIS' , style={'width': '20%'}) ,
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
    Input('adresse-input', 'value'),
)
def update_data(n_clicks,adresse):
    # print(f"adresse {adresse}")
    # print(f"n_clicks {n_clicks}")

    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        longitude = create_long_lat({'q':{adresse}})[0]
        latitude = create_long_lat({'q':{adresse}})[1]
        # print(f"longitude: {longitude}")
        # print(f"latitude: {latitude}")
        # longitude, latitude = create_long_lat({'q': {adresse}})
        # Mettez à jour les données en fonction de l'année sélectionnée
        data = estimation_prix_m2(longitude, latitude)
        # print(f"data: {data}")
        data2 = [[longitude, latitude, round(data.get('predicted_prix_m2'), 2)]]
        # print(f"data2 {data2}")
        df = pd.DataFrame(data2, columns=['longitude', 'latitude', 'prix_m2'])

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
