import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Load and clean data
df = pd.read_csv('ALLDATA.csv')
df.replace('na', pd.NA, inplace=True)  # Replace 'na' with NaN
df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%m/%Y %H:%M')
df['peopleIn'] = pd.to_numeric(df['peopleIn'], errors='coerce')
df['peopleOut'] = pd.to_numeric(df['peopleOut'], errors='coerce')
df['nonNegDigActivity'] = pd.to_numeric(df['nonNegDigActivity'], errors='coerce')

# Create 'visitor_count' by adding 'peopleIn' and 'peopleOut'
df['visitor_count'] = df['peopleIn'].fillna(0) + df['peopleOut'].fillna(0)

# Create a Dash application
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Wildlife Park Data Visualization"),
    dcc.Graph(id='temperature-plot', figure=px.line(df, x='datetime', y='airTemperature', title='Air Temperature Over Time')),
    dcc.Graph(id='precipitation-plot', figure=px.line(df, x='datetime', y='precipitation', title='Precipitation Over Time')),
    dcc.Graph(id='visitor-plot', figure=px.line(df, x='datetime', y='visitor_count', title='Visitor Count Over Time')),
    dcc.Graph(id='digital-activity-plot', figure=px.line(df, x='datetime', y='nonNegDigActivity', title='Digital Activity Over Time'))
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
