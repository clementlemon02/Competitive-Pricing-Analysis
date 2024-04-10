import dash
import pandas as pd
from dash import html, dcc, dash_table
import mysql.connector
from dash.dependencies import Input, Output
import plotly.express as px

dash.register_page(__name__)

# Establish database connection
connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password=''
)

# Fetch data from SQL database
cp_query = """
    SELECT attraction, ticket, price
    FROM (
        SELECT attraction, ticket, price,
                AVG(price) OVER (PARTITION BY attraction) AS mean_price
        FROM competitor.competitor_prices_dataset
    ) AS cp
    ORDER BY mean_price;
"""
cp_df = pd.read_sql(cp_query, connection)

connection.close()

# Convert 'attraction' column to categorical data type
cp_df['attraction'] = cp_df['attraction'].astype('category')

# Create box plot
cp_fig = px.strip(cp_df, x='attraction', y='price', color='attraction', title='Prices by Attraction',
             hover_data=['ticket', 'price'],
             labels={
                "attraction": "Attraction",
                "price": "Price"
             })
# Add horizontal lines for adult and child prices
cp_fig.add_hline(y=20, line=dict(color='blue', width=2, dash='dash'), annotation_text='Adult', annotation_position='top right')
cp_fig.add_hline(y=17, line=dict(color='red', width=2, dash='dash'), annotation_text='Child', annotation_position='bottom right')

# Dash layout
layout = html.Div([
    html.H1('Data Visualizations'),
    # Competitors Pricings
    html.H3('Competitors Pricings'),
    dcc.Graph(figure=cp_fig)
])