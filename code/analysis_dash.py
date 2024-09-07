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

# Group by date and calculate daily aggregates with max temperature
daily_df = df.set_index('datetime').resample('D').agg({
    'nonNegDigActivity': 'sum',
    'relativeHumidity': 'mean',
    'airTemperature': 'max',
    'precipitation': 'sum',
    'peopleIn': 'sum'
}).reset_index()

people_df = df.set_index('datetime').resample('D').agg({
    'relativeHumidity': 'mean',
    'airTemperature': 'max',
    'precipitation': 'sum',
    'peopleIn': 'sum'
})
people_df = people_df.dropna(subset=['peopleIn'])

dig_df = df.set_index('datetime').resample('D').agg({
    'relativeHumidity': 'mean',
    'airTemperature': 'max',
    'precipitation': 'sum',
    'nonNegDigActivity': 'sum'
})
dig_df = dig_df.dropna(subset='nonNegDigActivity')

# Calculate correlation matrix
correlation_matrix = daily_df[['nonNegDigActivity', 'peopleIn', 'airTemperature', 
                               'precipitation', 'relativeHumidity']].corr()
corr_dig_df = dig_df[['nonNegDigActivity', 'airTemperature', 'precipitation', 'relativeHumidity']].corr()
corr_people_df = people_df[['peopleIn', 'airTemperature', 'precipitation', 'relativeHumidity']].corr()

# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up graphs
max_air_temp = px.line(daily_df, x='datetime', y='airTemperature', title='Max Air Temperature Per Day')

total_visitor = px.line(daily_df, x='datetime', y='peopleIn', title='Total Visitor Count Per Day')

total_dig = px.line(daily_df, x='datetime', y='nonNegDigActivity', title='Total Digital Activity Per Day')

dig_v_airtemp = px.scatter(dig_df, x='nonNegDigActivity', y='airTemperature', title='Daily Digital Activity vs Max Air Temperature')


dig_v_humid = px.scatter(dig_df, x='nonNegDigActivity', y='relativeHumidity', 
                                                    title='Daily Digital Activity vs relative Humidity',
                                                    labels={'nonNegDigActivity': 'Digital Activity', 'relativeHumidity': 'Relative Humidity' })

dig_v_rain = px.scatter(dig_df, x='nonNegDigActivity', y='precipitation', 
                                                    title='Daily Digital Activity vs Precipitation',
                                                    labels={'nonNegDigActivity': 'Digital Activity', 'precipitation': 'Total Daily Precipitation'})

peopleIn_v_airtemp = px.scatter(people_df, x='peopleIn', y='airTemperature', 
                                                        title='Daily People In vs Max Air Temperature',
                                                        labels={"nonNegDigActivity": "Digital Activity", "airTemperature": "Maximum Air Temperature"})

peopleIn_v_humid = px.scatter(people_df, x='peopleIn', y='relativeHumidity', 
                                                        title='Daily People In vs Relative Air Humidity',
                                                        labels={'peopleIn': 'Total Visitors', 'relativeHumidity': 'Relative Humidity'})

peopleIn_v_rain = px.scatter(people_df, x='peopleIn', y='precipitation', 
                                                        title='Daily People In vs Precipitation',
                                                        labels={'peopleIn': 'Total Visitors', 'precipitation': 'Total Daily Precipitation'})


# App layout
app.layout = html.Div([
    html.H1("Wildlife Park Data Visualization"),
    html.H2("Correlation Matrix"),
    # Display the correlation matrices as preformatted text
    dbc.Row([
        dbc.Col(html.Pre(correlation_matrix.to_string()), md=12),
    ]),
    dbc.Row([
        dbc.Col(html.Pre(corr_dig_df.to_string()), md=12),
    ]),
    dbc.Row([
        dbc.Col(html.Pre(corr_people_df.to_string()), md=12),
    ]),
    # General Stats row
    dbc.Row([
        dbc.Col(dcc.Graph(id='total_visitor', figure=total_visitor), md=6),
        dbc.Col(dcc.Graph(id='visitor-plot', figure=total_dig), md=6),
    ]),
    # Digital Activity Row
    dbc.Row([
        dbc.Col(dcc.Graph(id='dig_v_airtemp', figure=dig_v_airtemp), md=4),
        dbc.Col(dcc.Graph(id='dig_v_humid', figure=dig_v_humid), md=4),
        dbc.Col(dcc.Graph(id='dig_v_rain', figure=dig_v_rain), md=4)
    ]),
    # PeopleIn row
    dbc.Row([
        dbc.Col(dcc.Graph(id='peopleIn_v_airtemp', figure=peopleIn_v_airtemp), md=4),
        dbc.Col(dcc.Graph(id='peopleIn_v_humid', figure=peopleIn_v_humid), md=4),
        dbc.Col(dcc.Graph(id='peopleIn_v_rain', figure=peopleIn_v_rain), md=4)
    ])
], fluid=True)



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
