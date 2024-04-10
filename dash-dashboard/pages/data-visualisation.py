import dash
import pandas as pd
from dash import html, dcc, dash_table
import mysql.connector
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime

dash.register_page(__name__)

# Establish database connection
connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='Lks6712281119@'
)
'''
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
'''
ridership_month_query = '''
    SELECT Period, Ridership,Date
    FROM dsa3101.ridershipbymonth;
    '''

ridership_hour_query = '''
    SELECT Hour, Ridership as Percentile
    FROM dsa3101.ridershipbyhour;
    '''

nationalities_query = '''
    SELECT Nationality, Percentile
    FROM dsa3101.keynationalities;
    '''

rm_df = pd.read_sql(ridership_month_query, connection)
rh_df = pd.read_sql(ridership_hour_query, connection)
nationality_df = pd.read_sql(nationalities_query, connection)

connection.close()

# Convert date string to datetime object
rm_df['Date'] = pd.to_datetime(rm_df['Date'], format='%m/%d/%Y')

# Extract month and year
rm_df['Month'] = rm_df['Date'].dt.strftime('%B')
rm_df['Year'] = rm_df['Date'].dt.year

monthly_avg = rm_df.groupby(['Month'], as_index=False)['Ridership'].mean()

rm_fig=px.line(monthly_avg, x='Month', y='Ridership', title='Monthly Average Ridership')
rh_fig=px.line(rh_df, x='Hour', y='Percentile', title='Hourly Average Ridership')
nationality_fig=px.bar(nationality_df, x='Nationality', y='Percentile', title='Nationalities')


# Dash layout
layout = html.Div([
    html.H1('Data Visualizations'),
    # Competitors Pricings
    #html.H3('Competitors Pricings'),
    #dcc.Graph(figure=cp_fig),
    dcc.Graph(figure=rm_fig),
    dcc.Graph(figure=rh_fig),
    dcc.Graph(figure=nationality_fig)
])


'''
to add dropdown to rm_df, in the process of debugging
# Calculate monthly average ridership
monthly_avg = rm_df.groupby(['Month', 'Year'], as_index=False)['Ridership'].mean()

# Create line plot for monthly average ridership
rm_fig = px.line(monthly_avg, x='Month', y='Ridership', title='Monthly Average Ridership')

dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in rm_df['Year'].unique()],
        value=[rm_df['Year'].min()],  # Default to the minimum year
        multi=True  # Allow multiple selections
    ),

# Define callback to update hourly ridership figure based on selected years
@app.callback(
    Output('hourly-ridership-fig', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_hourly_ridership(selected_years):
    filtered_data = rh_df[rh_df['Year'].isin(selected_years)]
    fig = px.line(filtered_data, x='Hour', y='Ridership', title='Hourly Ridership')
    return fig

    '''