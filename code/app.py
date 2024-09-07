import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np


# Load and clean data
df = pd.read_csv('ALLDATA.csv')
df.replace('na', pd.NA, inplace=True)
df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%m/%Y %H:%M')
df['peopleIn'] = pd.to_numeric(df['peopleIn'], errors='coerce')
df['peopleOut'] = pd.to_numeric(df['peopleOut'], errors='coerce')
df['nonNegDigActivity'] = pd.to_numeric(df['nonNegDigActivity'], errors='coerce')
df['relativeHumidity'] = pd.to_numeric(df['relativeHumidity'], errors='coerce')
df['pademelon'] = pd.to_numeric(df['pademelon'], errors='coerce')
df['red_necked_wallaby'] = pd.to_numeric(df['red_necked_wallaby'], errors='coerce')
df['great_barred_frog'] = pd.to_numeric(df['great_barred_frog'], errors='coerce')
df['yellow_throated_scrubwren'] = pd.to_numeric(df['yellow_throated_scrubwren'], errors='coerce')
df['noisy_pitta'] = pd.to_numeric(df['noisy_pitta'], errors='coerce')

# Group by date and calculate daily aggregates with max temperature
daily_df = df.set_index('datetime').resample('D').agg({
    'nonNegDigActivity': 'sum',
    'relativeHumidity': 'mean',
    'airTemperature': 'max',
    'precipitation': 'sum',
    'peopleIn': 'sum',
    'windSpeed': 'mean',
    'pademelon': 'sum',
    'red_necked_wallaby': 'sum',
    'great_barred_frog': 'sum',
    'yellow_throated_scrubwren': 'sum',
    'noisy_pitta': 'sum'
}).reset_index()

people_df = df.set_index('datetime').resample('D').agg({
    'relativeHumidity': 'mean',
    'airTemperature': 'max',
    'precipitation': 'sum',
    'peopleIn': 'sum',
    'windSpeed': 'mean',
    'pademelon': 'sum',
    'red_necked_wallaby': 'sum',
    'great_barred_frog': 'sum',
    'yellow_throated_scrubwren': 'sum',
    'noisy_pitta': 'sum'
})
people_df = people_df.dropna(subset=['peopleIn'])

dig_df = df.set_index('datetime').resample('D').agg({
    'relativeHumidity': 'mean',
    'airTemperature': 'max',
    'precipitation': 'sum',
    'nonNegDigActivity': 'sum',
    'windSpeed': 'mean',
    'pademelon': 'sum',
    'red_necked_wallaby': 'sum',
    'great_barred_frog': 'sum',
    'yellow_throated_scrubwren': 'sum',
    'noisy_pitta': 'sum'
})
dig_df = dig_df.dropna(subset=['nonNegDigActivity'])

# Calculate correlation matrix
correlation_matrix = daily_df[['nonNegDigActivity', 'peopleIn', 'airTemperature', 
                               'precipitation', 'relativeHumidity', 'windSpeed',
                               'pademelon','red_necked_wallaby','great_barred_frog','yellow_throated_scrubwren',
                               'noisy_pitta']].corr()
corr_dig_df = dig_df[['nonNegDigActivity', 'airTemperature', 'precipitation', 'relativeHumidity', 'windSpeed',
                      'pademelon','red_necked_wallaby','great_barred_frog','yellow_throated_scrubwren','noisy_pitta']].corr()
corr_people_df = people_df[['peopleIn', 'airTemperature', 'precipitation', 'relativeHumidity', 'windSpeed',
                            'pademelon','red_necked_wallaby','great_barred_frog','yellow_throated_scrubwren','noisy_pitta']].corr()

# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Example animals: 'pademelon','red_necked_wallaby','great_barred_frog','yellow_throated_scrubwren','noisy_pitta'
# App layout
app.layout = dbc.Container([
    html.H1("Wildlife Park Data Visualization"),
    html.H1('General Statistics'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.line(daily_df, x='datetime', y='airTemperature', title='Max Air Temperature Per Day')), md=6),
        dbc.Col(dcc.Graph(figure=px.line(daily_df, x='datetime', y='peopleIn', title='Total Visitor Count Per Day')), md=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.line(daily_df, x='datetime', y='nonNegDigActivity', title='Total Digital Activity Per Day')), md=12)
    ]),
    html.H2('Digital Activity'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.scatter(dig_df, x='nonNegDigActivity', y='airTemperature', title='Daily Digital Activity vs Max Air Temperature')), md=6),
        dbc.Col(dcc.Graph(figure=px.scatter(dig_df, x='nonNegDigActivity', y='windSpeed', title='Daily Digital Activity vs Mean Wind Speed')), md=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.scatter(dig_df, x='nonNegDigActivity', y='relativeHumidity', title='Daily Digital Activity vs Relative Humidity')), md=6),
        dbc.Col(dcc.Graph(figure=px.scatter(dig_df, x='nonNegDigActivity', y='precipitation', title='Daily Digital Activity vs Precipitation')), md=6)
    ]),
    html.H2('People In'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.scatter(people_df, x='peopleIn', y='airTemperature', title='Daily People In vs Max Air Temperature')), md=6),
        dbc.Col(dcc.Graph(figure=px.scatter(people_df, x='peopleIn', y='windSpeed', title='Daily People In vs Mean Wind Speed')), md=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.scatter(people_df, x='peopleIn', y='relativeHumidity', title='Daily People In vs Relative Humidity')), md=6),
        dbc.Col(dcc.Graph(figure=px.scatter(people_df, x='peopleIn', y='precipitation', title='Daily People In vs Precipitation')), md=6)
    ]),
    html.H2('Animal Sightings'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.scatter(dig_df, x='nonNegDigActivity', y='pademelon',
                                            title='Daily Digital Activity vs Total Pademelon Sightings',
                                            labels = {'nonNegDigitalActivity': 'Digital Activity','pademelon': 'Pademelon Sightings'})), md=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.scatter(dig_df, x='nonNegDigActivity', y='red_necked_wallaby',
                           title='Daily Digital Activity vs Total Red Necked Wallaby Sightings',
                           labels = {'nonNegDigActivity': 'Digital Activity',
                                     'red_necked_wallaby': 'Red Necked Wallaby Sightings'})), md=12)
    ])
], fluid=True)  # Ensure the container is fluid

# Deploy local port to internet. WARNING: Temporary only. This is a major security risk.
# For proper development, set up actual server. This is only for competition judging.
"""from pyngrok import ngrok
def start_ngrok():
    ngrok_tunnel = ngrok.connect(8050)
    print(' * Tunnel URL:', ngrok_tunnel.public_url)"""

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
    #start_ngrok()
    #app.run_server(debug=True, port=8050, use_reloader=False)
