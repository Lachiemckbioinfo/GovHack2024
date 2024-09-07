import dash
from dash import html, dcc
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
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Wildlife Park Data Visualization"),
    html.H2("Correlation Matrix"),
    # Display the correlation matrices as preformatted text
    html.Pre(correlation_matrix.to_string()), 
    html.Pre(corr_dig_df.to_string()), 
    html.Pre(corr_people_df.to_string()), 
    dcc.Graph(id='temperature-plot', figure=px.line(daily_df, x='datetime', y='airTemperature', title='Max Air Temperature Per Day')),
    dcc.Graph(id='visitor-plot', figure=px.line(daily_df, x='datetime', y='peopleIn', title='Total Visitor Count Per Day')),
    dcc.Graph(id='digital-activity-plot', figure=px.line(daily_df, x='datetime', y='nonNegDigActivity', title='Total Digital Activity Per Day')),
    dcc.Graph(id='scatter-temp', figure=px.scatter(dig_df, x='nonNegDigActivity', y='airTemperature', title='Daily Digital Activity vs Max Air Temperature')),
    dcc.Graph(id='scatter-dig-humid', figure=px.scatter(dig_df, x='nonNegDigActivity', y='relativeHumidity', title='Daily Digital Activity vs relative Humidity')),
    dcc.Graph(id='scatter-people-temp', figure=px.scatter(people_df, x='peopleIn', y='airTemperature', title='Daily People In vs Max Air Temperature')),
    dcc.Graph(id='scatter-people-humid', figure=px.scatter(people_df, x='peopleIn', y='relativeHumidity', title='Daily People In vs Relative Air Humidity'))
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
