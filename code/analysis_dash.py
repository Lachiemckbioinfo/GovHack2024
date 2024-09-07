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



# Group by date and calculate daily aggregates
daily_df = df.set_index('datetime').resample('D').agg({
    'nonNegDigActivity': 'sum',
    'relativeHumidity': 'mean',
    'airTemperature': 'mean',
    'precipitation': 'sum',
    'peopleIn': 'sum'
}).reset_index()

# Calculate correlation matrix
correlation_matrix = daily_df[['nonNegDigActivity', 'precipitation', 'airTemperature', 'relativeHumidity', 'peopleIn']].corr()

# Create a Dash application
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Wildlife Park Data Visualization"),
    html.H2("Correlation Matrix"),
    html.Pre(correlation_matrix.to_string()),
    dcc.Graph(id='temperature-plot', figure=px.line(daily_df, x='datetime', y='airTemperature', title='Average Air Temperature Per Day')),
    dcc.Graph(id='precipitation-plot', figure=px.line(daily_df, x='datetime', y='precipitation', title='Total Precipitation Per Day')),
    dcc.Graph(id='visitor-plot', figure=px.line(daily_df, x='datetime', y='peopleIn', title='Total Visitor Count Per Day')),
    dcc.Graph(id='digital-activity-plot', figure=px.line(daily_df, x='datetime', y='nonNegDigActivity', title='Total Digital Activity Per Day')),
    dcc.Graph(id='scatter-plot-temp', figure=px.scatter(daily_df, x='nonNegDigActivity', y='airTemperature', title='Daily Digital Activity vs Average Air Temperature')),
    dcc.Graph(id='scatter-plot-precip', figure=px.scatter(daily_df, x='nonNegDigActivity', y='precipitation', title='Daily Digital Activity vs Total Precipitation')),
    dcc.Graph(id='scatter-plot-humid', figure=px.scatter(daily_df, x='nonNegDigActivity', y='relativeHumidity', title='Daily Digital Activity vs Average Humidity')),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
